from flask_restx import Resource, Namespace
from flask import request
from app.utils import auth_required, admin_required
from app.container import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        return director_service.get_all(), 200

    @admin_required
    def post(self):
        new_data = request.json
        director_service.create(new_data)
        return "Created", 201


@director_ns.route('/<int:item_id>')
class DirectorView(Resource):
    @auth_required
    def get(self, item_id):
        return director_service.get_one(item_id), 200

    @admin_required
    def put(self, item_id):
        new_data = request.json
        new_data["id"] = item_id
        director_service.update(new_data)
        return "No Content", 204

    @admin_required
    def delete(self, item_id):
        director_service.delete(item_id)
        return "No Content", 204