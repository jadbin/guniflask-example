# coding=utf-8

from flask import render_template
from guniflask.web import blueprint, websocket, get_route
from starlette.websockets import WebSocket


@blueprint('/')
class ChatController:
    @get_route('/chat')
    def chat_page(self):
        return render_template('chat.html')

    @websocket('/ws/chat')
    async def chat(self, socket: WebSocket):
        await socket.accept()
        while True:
            data = await socket.receive_text()
            await socket.send_text(f"Message was: {data}")
