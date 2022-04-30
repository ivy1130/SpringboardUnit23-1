from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name = 'TestFirst', last_name = 'TestLast', img_url = "https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Users', html)
            self.assertIn('TestFirst TestLast', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add New User', html)

    def test_add_user_success(self):
        with app.test_client() as client:
            d = {"first-name" : "TestFirstTwo", "last-name" : "TestLastTwo", "img-url" : ""}
            resp = client.post('/users/new', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstTwo TestLastTwo', html)

    def test_view_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst TestLast', html)
            self.assertIn('"https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png"', html)

    def test_update_user_details(self):
        with app.test_client() as client:
            d = {"first-name" : "TestFirstUpdated", "last-name" : "TestLastTwo", "img-url" : ""}
            resp = client.post(f'/users/{self.user_id}/edit', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstUpdated TestLast', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>\n    \n</ul>', html)



