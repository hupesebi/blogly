
from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTest(TestCase):

    def setUp(self):
        Post.query.delete()
        User.query.delete()
        user =User(first_name = "Hans", last_name='Maier', image_url='https://images.pexels.com/photos/1933873/pexels-photo-1933873.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')
        db.session.add(user)
        db.session.commit()
        post = Post(title='A title', content='Great stuff', user_id= user.id)
        db.session.add(post)	
        db.session.commit()

        self.user_id = user.id

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hans', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Maier', html)
            self.assertIn('Hans', html)

    def test_add_user(self):
        with app.test_client() as client:
            client.post('/users/newuser', 
                        data={'first_name': 'Test', 'last_name': 'Name', 'image_url': 'www.test.com'})
            user = User.query.filter_by(last_name = 'Name').first()

            self.assertEqual(user.last_name, 'Name')
            self.assertEqual(user.image_url, 'www.test.com')

    def test_edit_user(self):
        with app.test_client() as client:
            client.post(f'users/{self.user_id}/edit',
                    data={'first_name': 'Hans', 'last_name': 'Maier', 'image_url': 'www.test.com'})
            user = User.query.get_or_404(self.user_id)

            self.assertEqual(user.first_name, 'Hans')
            self.assertEqual(user.image_url, 'www.test.com')
    
    def test_delete_user(self):
        with app.test_client() as client:
            client.get(f'/users/{self.user_id}/delete')
            user = User.query.get(self.user_id)
            self.assertFalse(user)

    def test_show_new_post_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            user = User.query.get(self.user_id)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name, html)
    
    def test_add_new_post(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', 
			data={'title': 'Test title', 'content': 'Test stuff', 'user_id': self.user_id})
            
            user = User.query.get(self.user_id)
            post = Post.query.filter_by(title = 'Test title').first()

			# Redirect to check if post got posted.
            
            html = client.get(f'/posts/{post.id}').get_data(as_text=True)
            
            self.assertIn('Test title', html)
            self.assertIn('Test stuff', html)
            self.assertIn(user.full_name, html)
    





