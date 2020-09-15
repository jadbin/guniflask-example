# coding=utf-8

from os.path import join, dirname
from typing import Union

from guniflask.context import service, component

from guniflask_example.config.jwt_config import jwt_manager

template_folder = join(dirname(dirname(__file__)), 'templates')
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
            token = jwt_manager.create_access_token(
                user_info['authorities'],
                username=username
            )
            return {
                'access_token': token,
                'username': username
            }
