# coding=utf-8

import logging

from guniflask.context import service
from guniflask.scheduling import async_run
from guniflask.config import settings

log = logging.getLogger(__name__)


@service
class AsyncService:

    @async_run
    def example_async_run(self):
        import time
        log.info(f'[{settings["project_name"]}]: async run start, will sleep 10 seconds ({self.__module__})')
        time.sleep(10)
        log.info(f'[{settings["project_name"]}]: async run end ({self.__module__})')
