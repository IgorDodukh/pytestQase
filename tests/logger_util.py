import logging.config

logging_config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '{asctime} - {name}:{lineno} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}

logging.config.dictConfig(logging_config)


def get_logger(name):
    return logging.getLogger(name)
