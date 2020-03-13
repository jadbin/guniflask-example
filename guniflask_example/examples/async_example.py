# coding=utf-8

import logging

from guniflask.context import service
from guniflask.scheduling import async_run

log = logging.getLogger(__name__)


@service
class AsyncService:

    @async_run
    def example_async_run(self):
        import time
        log.info('async run start, will sleep 10 seconds (%s)', self.__module__)
        time.sleep(10)
        log.info('async run end (%s)', self.__module__)
