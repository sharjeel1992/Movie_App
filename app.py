from flask import Flask, render_template, request, url_for, redirect
import requests
from dataManager import SQLiteDataManager
from dataManager import db, Movies
from api import api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jsk1992/PycharmProjects/movieweb_update/dataManager/table' \
                                        '.sqlite'
db.init_app(app)

data_manager = SQLiteDataManager('table.sqlite')
app.register_blueprint(api_bp, url_prefix='/api')

API = f'http://www.omdbapi.com/?apikey=c61fc86&t='


@app.route('/')
def home():
    """This route is to simply render the homepage.html"""
    return render_template('homepage.html')


@app.route('/users')
def list_users():
    """This route is to show all the users saved in our database"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    This route is for movies of a specific user based on user id and will render movies.html page
    on the screen
    """
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    This route is to add user to the database.If request method is post it will add user and redirect
    to list of users.If request method is get it will display a html page to add new user to database
    """
    if request.method == 'POST':
        name = request.form.get('name')
        data_manager.add_user(name)
        return redirect(url_for('list_users'))
    else:
        return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=["POST", "GET"])
def add_movie(user_id):
    """
     This route is to add movie to the database for a specific user based on user id.It handles both
     get and post requests.Also based on movie title we will fetch data of that movie using API and
     store that data in our database
     """
    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        omdb_api_url = API + movie_title
        response = requests.get(omdb_api_url)
        movie_data = response.json()
        year_value = movie_data.get('Year', '')
        publication_year = int(year_value.split('–')[0]) if '–' in year_value else int(year_value)
        movie_rating = float(movie_data.get('imdbRating', 0))
        cover_image = movie_data.get('Poster', '')  # Get the cover_image URL from the response
        new_movie = Movies(movie_title=movie_title, publication_year=publication_year,
                           movie_rating=movie_rating, user_id=user_id, cover_image=cover_image)
        data_manager.add_movie(new_movie)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    This route is for updating a specific movie of a specific user, so we are using both
    user id and movie id.
     """
    movie = data_manager.get_movie_id(movie_id)
    if request.method == 'POST':
        movie_name = request.form.get('name')
        year = request.form.get('year')
        rating = request.form.get('rating')
        data_manager.update_movie(movie_id, movie_name, year, rating)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return render_template('update_movie.html', movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    This route is established to delelte a spefic movie of a specific user.It only hanles post requests
    .Any other way of request will result in rendring a error template page
    """
    success = data_manager.delete_movie(movie_id)
    if success:
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return render_template('error.html', message='Movie not found')


@app.route('/review/<int:movie_id>', methods=['GET', 'POST'])
def add_review(movie_id):
    """
    This route is established to handle reviews on a specific movie.Get method is for rendering
    add review template while post is to get that data and pass it function to be saved in our database
    """
    user_id = request.args.get('user_id')
    if request.method == 'POST':
        review_text = request.form.get('review_text')
        cust_rating = int(request.form.get('rating'))
        data_manager.movie_review(user_id, movie_id, review_text, cust_rating)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        movie = data_manager.get_movie_id(movie_id)
        return render_template('add_review.html', movie=movie, user_id=user_id)


@app.errorhandler(404)
def page_not_found(e):
    """This route is for to handle page not found error"""
    return render_template(f'404.html {e}'), 404


if __name__ == '__main__':
    app.run(debug=True)
