# coding=utf-8

import json
from os.path import join, dirname

from flask import request, abort, jsonify, render_template
from guniflask.config import settings
from guniflask.security import has_any_role
from guniflask.web import blueprint, get_route, route

from guniflask_example.services.login_service import LoginService

template_folder = join(dirname(dirname(__file__)), 'templates')


@blueprint('/', template_folder=template_folder)
class AuthController:
    def __init__(self, login_service: LoginService):
        self.login_service = login_service

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'GET':
            return render_template('login.html')
        data = request.get_json()
        if data is not None:
            username = data.get('username')
            password = data.get('password')

            login_data = self.login_service.login(username, password)
            if login_data is None:
                abort(401)
            return jsonify(login_data)
        abort(403)

    @get_route('/settings')
    def get_settings(self):
        return render_template('settings.html')

    @get_route('/settings-table')
    @has_any_role('admin')
    def get_settings_table(self):
        def is_jsonable(v):
            try:
                json.dumps(v)
            except Exception:
                return False
            return True

        s = {}
        for k, v in settings.items():
            if is_jsonable(v):
                s[k] = v
        app_settings = [{'key': i, 'value': j} for i, j in s.items()]
        app_settings.sort(key=lambda k: k['key'])
        return render_template('settings_table.html', app_settings=app_settings)
