import requests
from flask import Blueprint, jsonify, request
from Web_Movie_App.dataManager import SQLiteDataManager
from Web_Movie_App.dataManager import Movies

api_bp = Blueprint('api', __name__)
data_manager = SQLiteDataManager('table.sqlite')
API = f'http://www.omdbapi.com/?apikey=c61fc86&t='


@api_bp.route('/users', methods=['GET'])
def get_users():
    """
    This functions handles api get request for users in our database and returns a json for all users
    in our database
    """
    users = data_manager.get_all_users()
    users_data = [{'user_id': user.id, 'username': user.username} for user in users]
    return jsonify(users_data)


@api_bp.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    This methods handles get requests from api for movies of a particular user and return all movies in form
     in json format
     """
    movies = data_manager.get_user_movies(user_id)
    movies_data = [{'movie_id': movie.movie_id, 'movie_title': movie.movie_title} for movie in movies]
    return jsonify(movies_data)


@api_bp.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    """
    This method allow api to send a post request to add a movie for a particular user in our database
    """
    client_data = request.json
    movie_title = client_data.get('movie_title')
    omdb_api_url = API + movie_title
    response = requests.get(omdb_api_url)
    movie_data = response.json()
    year_value = movie_data.get('Year', '')
    publication_year = int(year_value.split('–')[0]) if '–' in year_value else int(year_value)
    movie_rating = float(movie_data.get('imdbRating', 0))
    cover_image = movie_data.get('Poster', '')
    new_movie = Movies(movie_title=movie_title, publication_year=publication_year,
                       movie_rating=movie_rating, user_id=user_id, cover_image=cover_image)
    data_manager.add_movie(new_movie)
    if new_movie:
        return jsonify({'message': 'Movie added successfully'})
    else:
        return jsonify({'message': 'Movie could not be added'}, 400)


# WE CAN ADD MORE ROUTES HERE.....
