import os

from flask import Flask, request
import asyncio

from core.debug.errors_catcher import send_webhook
from routes.oauth2 import generate_link, generate_auth_data, check_linked, discord_auth_redirect
from routes.sponsors import sponsor_info

template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)


@app.route('/api/auth/<user_id>', methods=['POST'])
def generate_auth_data_route(user_id):
    return generate_auth_data(user_id, request.args.get('key'))


@app.route('/api/auth/<user_id>', methods=['GET'])
def check_linked_route(user_id):
    return asyncio.run(check_linked(user_id))


@app.route('/api/auth/redirect', methods=['GET'])
def discord_auth_redirect_route():
    return asyncio.run(discord_auth_redirect(request.args.get('code'), request.args.get('state')))


@app.route('/api/sponsors/<user_id>', methods=['GET'])
def sponsor_info_handler_route(user_id):
    return sponsor_info(user_id)


if __name__ == '__main__':
    with app.app_context():
        link = generate_link('ffc80662-6c8d-4c67-a729-658717508eb1')
        asyncio.run(send_webhook('Тестовая ссылка: ' + link, is_important=True))

    app.run(host='0.0.0.0', port=8080, debug=True)
