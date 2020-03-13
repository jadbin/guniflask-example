# coding=utf-8

"""
关于Blueprint、单例模式、依赖注入、用户认证相关的页面
http://localhost:8000/auth-example/
"""

import json
from os.path import join
from typing import Union

from flask import request, abort, jsonify, render_template

from guniflask.config import settings
from guniflask.security import roles_required
from guniflask.web import blueprint, get_route, route
from guniflask.context import service, component
from guniflask.security import jwt_manager

from guniflask_example.config import template_folder

static_folder = join(template_folder, 'static')


@component
class UserStore:
    accounts = {
        'root': {
            'password': '123456',
            'authorities': ['role_admin', 'role_user']
        }
    }

    def get_user(self, username: str):
        return self.accounts.get(username)


@service
class LoginService:
    def __init__(self, user_store: UserStore):
        self.user_store = user_store

    def login(self, username: str, password: str) -> Union[None, dict]:
        user_info = self.user_store.get_user(username)
        if user_info is None:
            return None

        if password == user_info['password']:
            token = jwt_manager.create_access_token(user_info['authorities'],
                                                    username=username)
            return {'access_token': token,
                    'username': username}


@blueprint('/auth-example',
           template_folder=template_folder,
           static_folder=static_folder,
           static_url_path='/static')
class AuthExample:
    def __init__(self, login_service: LoginService):
        """
        1. 优先选择名字一样并且符合"类型约束"
        2. 符合"类型约束"但名字不一样，如果有多个满足要求的会报错
        """
        self.login_service = login_service

    @get_route('/')
    def home_page(self):
        """
        Home page
        """
        return render_template('auth_example/index.html')

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        """
        Login app
        """
        if request.method == 'GET':
            return render_template('auth_example/login.html')
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
        """
        Settings page
        """
        return render_template('auth_example/settings.html')

    @get_route('/settings-table')
    @roles_required('admin')
    def get_settings_table(self):
        """
        Get settings of app
        """

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
        return render_template('auth_example/settings_table.html', app_settings=app_settings)
