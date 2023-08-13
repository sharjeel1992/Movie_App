from Web_Movie_App.dataManager.data_manager_interface import DataManagerInterface
from Web_Movie_App.dataManager.data_model import User, Movies, Review, db


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        """
        We can create instance with a database file name.In this project we have created one in app.py
        and api.py as well
        """
        self.db_file_name = db_file_name

    def get_all_users(self):
        """Method that will return all the users from the database"""
        return User.query.all()

    def get_user_movies(self, user_id):
        """This method returns all movies of a specific user based on user id."""
        user_movies = Movies.query.filter(Movies.user_id == user_id).all()
        return user_movies

    def get_movie_id(self, movie_id):
        """This method is to fetch id of specific movie and return it."""
        movie = Movies.query.get(movie_id)
        return movie

    def add_user(self, user):
        """This method is to add the new user to the database"""
        new_user = User(name=user)
        db.session.add(new_user)
        db.session.commit()

    def add_movie(self, movies):
        """This method is for adding new movie to the database"""
        db.session.add(movies)
        db.session.commit()

    def update_movie(self, movie_id, movie_title, publication_year, movie_rating):
        """This method is to update the a specific movie in our database associated with a specific user."""
        existing_movie = Movies.query.get(movie_id)
        if existing_movie:
            existing_movie.movie_title = movie_title
            existing_movie.publication_year = publication_year
            existing_movie.movie_rating = movie_rating
            db.session.commit()
            return True
        else:
            return False

    def delete_movie(self, movie_id):
        """
        This method is to find a movie based on its it and delete it from the database
        """
        movie = Movies.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        else:
            return False

    def movie_review(self, user_id, movie_id, review_text, cust_rating):
        """
        This method is to add a review in our database for a specific movie of a specific user
        """
        new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, cust_rating=cust_rating)
        db.session.add(new_review)
        db.session.commit()
