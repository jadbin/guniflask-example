# coding=utf-8

"""
定时任务的示例
"""

import logging

from guniflask.context import configuration
from guniflask.scheduling import scheduled

log = logging.getLogger(__name__)


@configuration
class SchedulingTask:
    """
    @configuration装饰的类为单例模式
    """

    @scheduled(interval=5)
    def example_scheduled_task(self):
        """
        通过cron参数配置crontab格式的定时任务
        通过interval参数配置固定间隔的定时任务，单位为秒
        """
        log.info('This is an example of scheduled task (%s)', self.__module__)
