import copy as _copy

__author__ = 'Michael'

__LOG_FORMAT = '[%(asctime)s %(name)s %(levelname)s] %(message)s'

__LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def __add_rotating_handlers(logging_dict, levels, name, namespace=None):
    if namespace is None:
        namespace = name

    logger = {
        'handlers': [],
        'propagate': False,
        'level': 'DEBUG'
    }

    for level in levels:
        key = "{}-{}".format(name, level)
        val = {
            'level': level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'logs/{}.log'.format(key),
            'encoding': 'UTF-8',
            'when': 'midnight'
        }
        logging_dict['handlers'][key] = val
        logger['handlers'].append(key)

    logging_dict['loggers'][namespace] = logger


def __add_rotating_handlers_all(logging_dict, levels):
    __add_rotating_handlers(logging_dict, levels, 'django')
    __add_rotating_handlers(logging_dict, levels, 'request', 'django.request')
    __add_rotating_handlers(logging_dict, levels, 'server', 'django.server')
    __add_rotating_handlers(logging_dict, levels, 'template', 'django.template')
    __add_rotating_handlers(logging_dict, levels, 'db', 'django.db')
    __add_rotating_handlers(logging_dict, levels, 'root', '')


__LOGGING_DICT_BASE = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': __LOG_FORMAT
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {}
}

LOGGING_DEBUG_ABOVE = _copy.deepcopy(__LOGGING_DICT_BASE)
__add_rotating_handlers_all(LOGGING_DEBUG_ABOVE, __LOG_LEVELS)

LOGGING_DEBUG_ONLY = _copy.deepcopy(__LOGGING_DICT_BASE)
__add_rotating_handlers_all(LOGGING_DEBUG_ONLY, __LOG_LEVELS[:1])

LOGGING_INFO_ABOVE = _copy.deepcopy(__LOGGING_DICT_BASE)
__add_rotating_handlers_all(LOGGING_INFO_ABOVE, __LOG_LEVELS[1:])

LOGGING_CONSOLE = _copy.deepcopy(__LOGGING_DICT_BASE)
LOGGING_CONSOLE['loggers'][''] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False
}
