command to run tests:

```shell
pytest --prometheus-pushgateway-url http://localhost:9091 \
       --prometheus-metric-prefix my_project_ \
       --prometheus-extra-label environment=staging \
       --prometheus-extra-label team=qa \
       --prometheus-job-name my_test_job

```