from flask import Flask, redirect, request, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def users():
    return redirect('/users')


@app.route('/users')
def show_users():
    """List all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users.html', users = users)


@app.route('/users/newuser')
def add_user_to_form():
    """Redirect to add user form"""

    return render_template('/users/newuser.html')


@app.route('/users/newuser', methods=['POST'])
def add_user():
    """Add user to db"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    newUser= User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(newUser)
    db.session.commit()
    return redirect ('/users')


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details of one user"""

    user = User.query.get_or_404(user_id)
    return render_template('/users/user.html', user = user)


@app.route ('/users/<int:user_id>/edit')
def user_edit_page(user_id):
    """Get user by id and render edit template"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user = user)


@app.route ('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Get user by id and update user details"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user from db"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')






