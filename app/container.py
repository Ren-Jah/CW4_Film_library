from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO
from app.dao.user import UserDAO
from app.dao.auth import AuthUserDAO

from app.services.directors_service import DirectorsService
from app.services.genres_service import GenresService
from app.services.movies_service import MoviesService
from app.services.users_service import UsersService
from app.services.auth_service import AuthUsersService

from app.database import db

#DAO
director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)
auth_user_dao = AuthUserDAO(session=db.session)

#Services
director_service = DirectorsService(dao=director_dao)
genre_service = GenresService(dao=genre_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
auth_user_service = AuthUsersService(dao=auth_user_dao)