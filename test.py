from unittest import TestCase
from app import app
from models import User, Post, db, connect_db
import flask


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


with app.app_context():
    connect_db(app)
    db.drop_all()
    db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        with app.app_context():
            Post.query.delete()
            User.query.delete()
            db.session.expire_on_commit = False

            user = User(first_name='unit', last_name='test', image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/640px-Image_created_with_a_mobile_phone.png')
            user_without_post = User(first_name='bad', last_name='user')
            db.session.add(user)
            db.session.add(user_without_post)
            db.session.commit()
            self.user_id = user.id
            self.user_without_post_id = user_without_post.id

            post = Post(title='test title', content='test content', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()     
            self.post_id = post.id
    
    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_full_name(self):
        user = User(first_name='full', last_name='name')
        self.assertEqual(user.full_name, "full name")         

    # test that home page loads
    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn('<button type="submit">Create User</button>', html)
            self.assertIn('<div class="col">\n        Users\n    </div>', html)
    
    def test_user_details(self):

        with app.test_client() as client:

            resp = client.get(f"/users/{self.user_id}/details/")
            html = resp.get_data(as_text=True)

            # created second user who has not made any posts
            no_post_resp = client.get(f"users/{self.user_without_post_id}/details")
            no_post_html = no_post_resp.get_data(as_text=True)
            
            # check to make sure posts do not show up for bad user
            self.assertNotIn('test title', no_post_html)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('unit test', html)
            self.assertIn('test title', html)

    def test_show_post(self):
        with app.test_client() as client:

            resp = client.get(f"/post/{self.post_id}/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('test title', html)
            self.assertIn('test content', html)

    def test_create_user(self):
        with app.test_client() as client:

            data = {"first_name": "created", "last_name": "user", "image_source": 'https://docs.python.org/3/_static/py.svg'}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('created user', html)

    def test_create_post(self):
        with app.test_client() as client:

            data = {"title": "new", "content": "post", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/post", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new', html)
    