from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    This is our user class that defines the table name users and also add data to the database
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Movies(db.Model):
    """
    This is our movie class that defines the table movies and also adds data to the database
    """
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_image = db.Column(db.String(500))

    def __repr__(self):
        return f'<Movies {self.movie_title}>'


class Review(db.Model):
    """
    This db Model is for creating a review table in our database and use it to store data via orm
    """
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    review_text = db.Column(db.String(1000), nullable=False)
    cust_rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Review{self.review_text}>'


class Director(db.Model):
    __tablename__ = 'directors'
    director_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dir_name = db.Column(db.String(30))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    birth_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Director{self.dir_name}>'


class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    genre_detail = db.Column(db.String(100))

    def __repr__(self):
        return f'<Genre{self.genre_detail}>'
