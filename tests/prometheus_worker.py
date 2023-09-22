import re

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from decorators import singleton


class TestStatus:
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@singleton
class PrometheusReport:
    def __init__(self, config):
        self.pushgateway_url = config.getoption('prometheus_pushgateway_url')
        self.prefix_name = config.getoption('prometheus_prefix_name')
        self.job_name = config.getoption('prometheus_job_name')
        self.registry = CollectorRegistry()
        self.start_date = None
        self.extra_labels = {item[0]: item[1] for item in
                             [i.split('=', 1) for i in config.getoption('prometheus_extra_label', default=[], skip=True)]}
        self.test_stats = {
            TestStatus.PASSED: {},
            TestStatus.FAILED: {},
            TestStatus.SKIPPED: {}
        }

    def build_report(self, test_name, execution_time, status, test_type, component_name):
        self.test_stats[status][test_name] = {"execution_time": execution_time,
                                              "status": status,
                                              "start_date": self.start_date,
                                              "test_type": test_type,
                                              "component": component_name}

    def _make_metric_name(self, name):
        unsanitized_name = f'{self.prefix_name}{name}'
        pattern = r'[^a-zA-Z0-9_]'
        replacement = '_'
        return re.sub(pattern, replacement, unsanitized_name)

    def _make_labels(self, testname):
        ret = self.extra_labels.copy()
        ret["test_name"] = testname
        return ret

    def _get_label_names(self):
        return self._make_labels("").keys()

    def add_metrics_for_tests_with_time(self, metric, testcases):
        for test_name, data in testcases.items():
            labels = self._make_labels(test_name)
            labels["start_date"] = data["start_date"]
            labels["test_type"] = data["test_type"]
            labels["component"] = data["component"]
            metric.labels(**labels).set(data["execution_time"])

    def build_gauge(self, status_type):
        gauge_metric = Gauge(self._make_metric_name(status_type),
                             f"Number of {status_type} tests",
                             labelnames=list(self._get_label_names()) + ["start_date", "test_type", "component"],
                             registry=self.registry)
        self.add_metrics_for_tests_with_time(gauge_metric, self.test_stats[status_type])

    def pytest_sessionfinish(self):
        for status in self.test_stats.keys():
            self.build_gauge(status)

        if (sum(len(v) for v in self.test_stats.values())) > 0:
            push_to_gateway(self.pushgateway_url, registry=self.registry, job=self.job_name)
