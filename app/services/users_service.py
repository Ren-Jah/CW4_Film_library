from app.dao.user import UserDAO
from app.dao.models.users import UserSchema
from app.utils import get_hash


class UsersService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, item_id):
        item_db = self.dao.get_one(item_id)
        item_serialized = UserSchema().dump(item_db)
        return item_serialized

    def get_one_by_email(self, item_data):
        item_db = self.dao.get_one_by_email(item_data)
        item_serialized = UserSchema().dump(item_db)
        return item_serialized

    def get_all(self):
        items_db = self.dao.get_all()
        items_serialized = UserSchema(many=True).dump(items_db)
        return items_serialized

    def create(self, item_data):
        item_in_schema = UserSchema().load(item_data)
        item_db = self.dao.create(item_in_schema)

    def update(self, new_data):
        self.dao.update(new_data)
        return self.dao

    def update_by_email(self, new_data):
        self.dao.update_by_email(new_data)
        return self.dao

    def delete(self, item_id):
        self.dao.delete(item_id)

    def hash_password(self, new_data):  # замена пароля на хэш пароля.
        if "password" in new_data:
            new_data["password"] = get_hash(new_data["password"])
            return new_data

    def hash_old_new_passwords(self, new_data):
        if "password_old" in new_data and "password_new" in new_data:
            new_data["password_old"] = get_hash(new_data["password_old"])
            new_data["password_new"] = get_hash(new_data["password_new"])
            return new_data
