
from flask import Flask, redirect, request, render_template
from models import db, connect_db, User, Post, Tag, PostTag
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
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('/users/user.html', user = user, posts = posts)


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


@app.route('/users/<int:user_id>/posts/new')
def show_add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new_post.html', user = user, tags= tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    newPost = Post(title = title, content = content, user_id = user_id, tags = tags)
    print (tags)
    db.session.add(newPost)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show details of one post"""

    post = Post.query.get_or_404(post_id)

    return render_template('posts/post.html',  post= post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('posts/edit.html', post = post, tags = tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_edited_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/tags/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('/tags/tags.html', tags = tags)


@app.route('/tags/new')
def show_add_tag():
    return render_template('/tags/new.html')


@app.route('/tags/new', methods=['POST'])
def add_tag():
    name = request.form['name']
    newTag = Tag (name = name)
    db.session.add(newTag)
    db.session.commit()
    return redirect('/tags/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tags/edit.html', tag = tag)


@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags/tags')

