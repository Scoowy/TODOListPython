import datetime


def __format_log(type_log: str, message: str):
    print('{:%Y-%m-%d %H:%M:%S} | {:^5} | {}'.format(datetime.datetime.now(), type_log, message))


def log_query(message: str):
    __format_log('QUERY', message.replace('\n', '').replace('\t', '').replace(' ' * 9, ''))


def log_error(message: str):
    __format_log('ERROR', message)


def log_info(message: str):
    __format_log('INFO', message)
