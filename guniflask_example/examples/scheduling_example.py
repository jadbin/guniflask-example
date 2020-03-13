# coding=utf-8

"""
定时任务的示例
"""

import logging

from guniflask.context import configuration
from guniflask.scheduling import scheduled
from guniflask.web import global_singleton

log = logging.getLogger(__name__)


@configuration
@global_singleton
class SchedulingTask:
    """
    @configuration装饰的类为单例模式
    @global_singleton装饰的类在服务器上具有全局唯一的单例，由于gunicorn在生产模式会启动多个worker，使用此装饰器可以实现只有一个worker下面的定时任务可以运行
    """

    @scheduled(interval=5)
    def example_scheduled_task(self):
        """
        通过cron参数配置crontab格式的定时任务
        通过interval参数配置固定间隔的定时任务，单位为秒
        """
        log.info('This is an example of scheduled task (%s)', self.__module__)
