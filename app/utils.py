import hashlib

from datetime import datetime, timedelta
import jwt
import calendar

from flask import request, abort

from app.dao.models.users import User
from app.constants import JWT_ALGORITHM, SECRET_HERE


def get_hash(password):
    """ Конвертирует полученный пароль в хэш пароля"""

    password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hash


def generate_tokens(data):
    """ Генерирует access_token, refresh_token в виде словаря"""

    # первый токен на 30 минут
    min30 = datetime.utcnow() + timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    data["refresh_token"] = False
    access_token = jwt.encode(payload=data, key=SECRET_HERE, algorithm=JWT_ALGORITHM)

    # второй токен на 30 дней
    days30 = datetime.utcnow() + timedelta(days=30)
    data["exp"] = calendar.timegm(days30.timetuple())
    data["refresh_token"] = True
    refresh_token = jwt.encode(payload=data, key=SECRET_HERE, algorithm=JWT_ALGORITHM)

    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


def decode_token(token):
    """ Общая функция декодирования токена по секретному ключу и алгоритму"""
    try:
        decoded_token = jwt.decode(jwt=token, key=SECRET_HERE, algorithms=[JWT_ALGORITHM])
        return decoded_token

    except Exception as e:
        abort(400)


def auth_required(func):
    """ Запрашивает авторизацию пользователя"""

    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        decoded_token_item = decode_token(token)

        if decoded_token_item["refresh_token"]:
            abort(400)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """ Проверяет является ли пользователь администратором"""

    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        decoded_token_item = decode_token(token)

        if decoded_token_item["role"] != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper


# Добавляем в ДБ таблицу User
def create_data(app, db):
    with app.app_context():
        db.drop_all()  # Очищаем таблицу, прежде чем вносить в нее данные
        db.create_all()

        u1 = User(email="vasya@gmail.com", password=get_hash("my_little_pony"), role="user")
        u2 = User(email="oleg@gmail.com", password=get_hash("qwerty"), role="user")
        u3 = User(email="olga@gmail.com", password=get_hash("P@ssw0rd"), role="admin")

        with db.session.begin():
            user_email_1 = "vasya@gmail.com"
            user_email_2 = "oleg@gmail.com"
            user_email_3 = "olga@gmail.com"
            user_selected_1 = db.session.query(User).filter(User.email == user_email_1).one_or_none()
            user_selected_2 = db.session.query(User).filter(User.email == user_email_2).one_or_none()
            user_selected_3 = db.session.query(User).filter(User.email == user_email_3).one_or_none()

            if not user_selected_1 or not user_selected_2 or not user_selected_3:
                db.session.add_all([u1, u2, u3])
