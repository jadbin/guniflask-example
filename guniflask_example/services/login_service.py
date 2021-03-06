# coding=utf-8

from typing import Union

import bcrypt
from guniflask.context import service, component

from guniflask_example.config.jwt_config import jwt_manager


@component
class UserStore:
    accounts = {
        'root': {
            'password': bcrypt.hashpw(b'123456', bcrypt.gensalt()),
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
        if bcrypt.checkpw(password.encode(), user_info['password']):
            token = jwt_manager.create_access_token(
                user_info['authorities'],
                username=username
            )
            return {
                'access_token': token,
                'username': username
            }
