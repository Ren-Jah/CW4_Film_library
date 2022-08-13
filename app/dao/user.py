from app.dao.models.users import User
from flask import request, abort


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, item_id):
        item = self.session.query(User).filter(User.id == item_id).one_or_none()
        return item

    def get_one_by_email(self, item_data):
        email = item_data.get("email")
        item = self.session.query(User).filter(User.email == email).one_or_none()
        return item

    def get_all(self):
        items_temp = self.session.query(User)

        page = request.args.get("page")
        print(f"Page in request is indicated as {page}")
        if page is not None:
            per_page_limit = 12
            page_int = int(page)
            items_paginated = items_temp.limit(per_page_limit).offset(page_int)
            return items_paginated
        else:
            items = items_temp.all()
            return items

    def create(self, item_data):
        new_data = User(**item_data)
        self.session.add(new_data)
        self.session.commit()
        return new_data

    def update(self, new_data):
        item_id = new_data.get("id")
        if item_id is None:
            abort(401)

        item = self.session.query(User).filter(User.id == item_id).update(new_data)
        self.session.commit()

    def update_by_email(self, new_data):
        email = new_data.get("email")
        if email is None:
            abort(401)

        item = self.session.query(User).filter(User.email == email).update(new_data)
        self.session.commit()

    def delete(self, item_id):
        item = self.get_one(item_id)
        self.session.delete(item)
        self.session.commit()