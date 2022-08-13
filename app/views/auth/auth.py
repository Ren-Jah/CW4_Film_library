from flask_restx import Resource, Namespace
from flask import request, abort
from app.container import auth_user_service
from app.utils import generate_tokens, decode_token

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        """
        позволяет пользователю залогиниться и получить 2 токена.
        :return:
        """
        new_data = request.json

        # Проверяем, что оба поля не пустые.
        email = new_data.get("email", None)
        password = new_data.get("password", None)
        if None in [email, password]:
            abort(400)

        # получаем хэш пароля пользователя.
        auth_user_service.hash_password(new_data)
        password_new_data = new_data.get("password")

        # получаем хэшированный пароль пользователя из БД.
        user_db = auth_user_service.get_one_by_email(new_data)
        password_db = user_db["password"]

        # проверяем, что хэши пароля пользователя из базы и при авторизации совпадают.
        if password_new_data != password_db:
            return {"error": "Неверные учётные данные"}, 401

        # генерируем токены.
        data = {
            "email": user_db["email"],
            "role": user_db["role"]
        }

        return generate_tokens(data), 201

    def put(self):
        """
        позволяет получить 2 обновленных токена.
        :return:
        """
        new_data = request.json

        refresh_token = new_data.get("refresh_token")
        if refresh_token is None:
            abort(400)

        access_token = new_data.get("access_token")
        if access_token is None:
            abort(400)

        decoded_token = decode_token(refresh_token)
        print(f"Decoded token - {decoded_token}")

        user_db = auth_user_service.get_one_by_email(decoded_token)
        if user_db is None:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "email": user_db["email"],
            "role": user_db["role"]
        }

        return generate_tokens(data), 201


@auth_ns.route('/register')
class AuthView(Resource):
    """ Позволяет пользователю зарегистрироваться"""
    def post(self):
        new_data = request.json

        user_role = new_data.get("role")
        if not user_role:
            abort(400)
        if user_role != "user":
            abort(400)

        auth_user_service.hash_password(new_data)
        auth_user_service.create(new_data)

        return "Created", 201