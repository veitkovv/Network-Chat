import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
TRACE_LOG_LEVEL = 'DEBUG'
TRACE_FILE_NAME = 'log/messages/trace.log'

logging.basicConfig(level=TRACE_LOG_LEVEL, format=LOG_FORMAT, filename=TRACE_FILE_NAME)


def trace_request(func):
    def wrap(request, *args, **kwargs):
        name = func.__name__
        logging.info('function %s - request - %s' % (name, request))
        return func(request, *args, **kwargs)

    return wrap
