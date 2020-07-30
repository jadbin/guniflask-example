# coding=utf-8

"""
欢迎界面，访问时触发异步调用
http://localhost:8000/hello-world/
"""

from flask import render_template

from guniflask_cli.config import _template_folder
from guniflask.web import blueprint, get_route

from guniflask_example.examples.async_example import AsyncService


@blueprint('/hello-world',
           template_folder=_template_folder)
class HelloWorld:

    def __init__(self, async_service: AsyncService):
        self._async_service = async_service

    @get_route('/')
    def home_page(self):
        """
        Will return the homepage immediately
        """
        self._async_service.example_async_run()
        return render_template('hello_world/index.html')
