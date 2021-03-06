from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


default_image_url = 'https://images.pexels.com/photos/1933873/pexels-photo-1933873.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'



class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = default_image_url)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')
    

class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True )
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True) 

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)

    posts = db.relationship ('Post', secondary = 'post_tags', backref = 'tags')

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)