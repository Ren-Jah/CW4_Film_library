from flask import request
from flask_restx import Resource, Namespace
from app.container import movie_service
from app.utils import auth_required, admin_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        return movie_service.get_all(), 200

    @admin_required
    def post(self):
        new_data = request.json
        movie_service.create(new_data)
        return "Created", 201


@movie_ns.route('/<int:item_id>')
class MovieView(Resource):
    @auth_required
    def get(self, item_id):
        return movie_service.get_one(item_id), 200

    @admin_required
    def put(self, item_id):
        new_data = request.json
        new_data["id"] = item_id
        movie_service.update(new_data)
        return "No Content", 204

    @admin_required
    def delete(self, item_id):
        movie_service.delete(item_id)
        return "No Content", 204