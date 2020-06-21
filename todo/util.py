import datetime

__string_log = '{} {}: {}'.format(datetime.datetime.now(), '{:^5}', '{}')


def log_query(message: str):
    print(__string_log.format('QUERY', message.replace('\n', '').replace('\t', '').replace(' ' * 9, '')))


def log_error(message: str):
    print(__string_log.format('ERROR', message))


def log_info(message: str):
    print(__string_log.format('INFO', message))
