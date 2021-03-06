# coding=utf-8

from os.path import join, dirname

from flask import render_template, send_from_directory
from guniflask.web import blueprint, get_route, RequestParam

static_folder = join(dirname(dirname(__file__)), 'templates', 'static')


@blueprint('/')
class HomeController:
    @get_route('/')
    def home_page(self):
        return render_template('index.html')

    @get_route('/static/<filename>')
    def static_file(self, filename=RequestParam):
        return send_from_directory(static_folder, filename)
