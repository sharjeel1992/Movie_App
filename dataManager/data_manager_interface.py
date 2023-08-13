from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """this method is an abstract function for getting all users from the database"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """This method is abstract function to get list of movies based on user's id"""
        pass

    @abstractmethod
    def get_movie_id(self, movie_id):
        """This method is abstract function to get single movie based on movie's id"""
        pass

    @abstractmethod
    def add_user(self, name):
        """This method will enforce the name parameter to fetch data from API"""
        pass

    @abstractmethod
    def add_movie(self, movies):
        """This method will be used to add movies"""
        pass

    @abstractmethod
    def update_movie(self, movie_id, movie_title, publication_year, movie_rating):
        """This method will force above-mentioned arguments to be implemented to update the movie"""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """This method will enforce the delete function"""
        pass

    @abstractmethod
    def movie_review(self, user_id, movie_id, review_text, rating):
        """
        This method is abstract method to enforce review method to the data manager
        """
        pass
