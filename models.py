from flask_sqlalchemy import SQLAlchemy

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


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    