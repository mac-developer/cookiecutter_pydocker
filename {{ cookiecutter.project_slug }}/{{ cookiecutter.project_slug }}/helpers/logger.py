import os
import json
import logging
import logging.config
import collections

from uuid import uuid4

CATALOG = {
    'dummy': {
        'type': 'app.dummy',
        'code': 'I-0001',
        'detail': 'Dummy Test Log Message'
    },
}


class CustomAdapter(logging.LoggerAdapter):
    catalog = {}

    @staticmethod
    def define(catalog):
        CustomAdapter.catalog.update(catalog)

    def process(self, msg, kwargs):
        base = self.catalog.get(msg, {
            'type': 'unknown',
            'code': 'X-XXXX',
            'detail': msg
        })
        od = collections.OrderedDict(sorted(kwargs['extra'].items()))
        nvp = ' '.join('{}={};'.format(k, v) for k, v in od.items())

        args = {
            'uuid': self.extra['uuid'],
            'type': base['type'],
            'code': base['code'],
            'detail': base['detail'],
            'nvp': nvp,
        }
        text = 'uuid={uuid}; type={type}; code={code}; detail={detail}; {nvp}'
        msg = text.format(**args)

        return msg, kwargs

    @staticmethod
    def setup_logging(
        default_path='../etc/logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
    ):
        """Setup logging configuration

        """
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)


if __name__ == '__main__':
    CustomAdapter.setup_logging()
    CustomAdapter.define(CATALOG)

    adapter = CustomAdapter(logging.getLogger(), extra={'uuid': str(uuid4())})

    adapter.error('error_test_message',
                  extra={'field1': 'value1', 'field2': 'value2'})

    adapter.info('info_test_message',
                 extra={'field1': 'value1', 'field2': 'value2'})

    adapter.warn('warning_test_message',
                 extra={'field1': 'value1', 'field2': 'value2'})

    adapter.debug('debug_test_message',
                  extra={'field1': 'value1', 'field2': 'value2'})
