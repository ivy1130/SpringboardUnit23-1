from unittest import TestCase
from datetime import datetime
from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

# I had db.dropall and db.createall in the top section only before any of the test classes. When running all the tests together, all the tests would fail. However, when running them individually, they would all work.

# Then I moved the db.dropall and db.createall into the setup of each of the classes, then when running them all together it worked.

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""
        db.drop_all()
        db.create_all()

        User.query.delete()

        user = User(first_name = 'TestFirst', last_name = 'TestLast', img_url = "https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        """Add sample post for sample user"""
        post = Post(title = 'Test Post', content = 'Test Content', created_at = datetime.now(), user_id = self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
    
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_users_list(self):
        """Show all users"""
        with app.test_client() as client:
            resp = client.get('/', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Users', html)
            self.assertIn('TestFirst TestLast', html)

    def test_add_user_form(self):
        """Show add user form"""
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add New User', html)

    def test_add_user_success(self):
        """User has been added to the user list"""
        with app.test_client() as client:
            d = {"first-name" : "TestFirstTwo", "last-name" : "TestLastTwo", "img-url" : ""}
            resp = client.post('/users/new', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstTwo TestLastTwo', html)

    def test_view_user_details(self):
        """Show user details"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst TestLast', html)
            self.assertIn('https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png', html)
            self.assertIn('Test Post', html)

    def test_update_user_details(self):
        """User details has been successfully updated"""
        with app.test_client() as client:
            d = {"first-name" : "TestFirstUpdated", "last-name" : "TestLastTwo", "img-url" : ""}
            resp = client.post(f'/users/{self.user_id}/edit', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstUpdated TestLast', html)

    def test_delete_user(self):
        """Delete user"""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>\n    \n</ul>', html)

class PostViewsTestCase(TestCase):
    """Tests for views for Posts"""
    def setUp(self):
        """Add sample user"""
        db.drop_all()
        db.create_all()

        User.query.delete()

        user = User(first_name = 'TestFirst', last_name = 'TestLast', img_url = "https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        # How can I reference the user.id in the UserViewsTestCase without fully copying this information over into the setUp for PostViewsTestCase?

        """Add sample post for sample user"""
        post = Post(title = 'Test Post', content = 'Test Content', created_at = datetime.now(), user_id = self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

        """Add sample tag for sample post"""
        tag = Tag(name = 'TestTag')
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id

        post.tags.append(tag)

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_add_post_form(self):
        """Show form to add a new post"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add New Post for TestFirst TestLast', html)

    def test_add_post_success(self):
        """New post has been added successfully with tags"""
        with app.test_client() as client:
            d = {"post-title" : "Test Post 2", "post-content" : "Test Content 2", "tags" : [self.tag_id]}
            client.post(f'/users/{self.user_id}/posts/new', data = d, follow_redirects = True)
            resp = client.get(f'/posts/2')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst TestLast', html)
            self.assertIn('Test Post 2', html)
            self.assertIn('TestTag', html)

    def test_view_post(self):
        """Show post"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            self.assertIn('Test Content', html)
            self.assertIn('TestFirst TestLast', html)
    
    def test_update_post(self):
        """Post has been successfully updated"""
        with app.test_client() as client:
            d = {"post-title" : "Updated Test Post", "post-content" : "Updated Test Content", "tags" : [self.tag_id]}
            resp = client.post(f'/posts/{self.post_id}/edit', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated Test Post', html)
            self.assertIn('Updated Test Content', html)
            self.assertIn('TestFirst TestLast', html)
            self.assertIn('TestTag', html)
    
    def test_delete_post(self):
        """Delete post, and it's removed from the user details"""
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>\n    \n</ul>', html)
    
    def test_deleted_user_posts(self):
        """Deleted user's posts are also deleted"""
        with app.test_client() as client:
            client.post(f'/users/{self.user_id}/delete', follow_redirects = True)
            resp = client.get(f'/posts/{self.post_id}')

            self.assertEqual(resp.status_code, 404)
    
    def test_deleted_tag_post(self):
        """Posts with deleted tags are still there"""
        with app.test_client() as client:
            client.post(f'/tags/{self.tag_id}/delete', follow_redirects = True)
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            self.assertIn('<p>Tags: \n    \n</p>', html)

class TagViewsTestCase(TestCase):
    """Tests for views for Posts"""
    def setUp(self):
        """Add sample user"""
        db.drop_all()
        db.create_all()

        User.query.delete()

        user = User(first_name = 'TestFirst', last_name = 'TestLast', img_url = "https://cdn.shopify.com/s/files/1/0344/6469/files/Screen_Shot_2017-04-05_at_9.15.16_PM.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        # How can I reference the user.id in the UserViewsTestCase without fully copying this information over into the setUp for PostViewsTestCase?

        """Add sample post for sample user"""
        post = Post(title = 'Test Post', content = 'Test Content', created_at = datetime.now(), user_id = self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

        """Add sample tag for sample post"""
        tag = Tag(name = 'TestTag')
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id

        post.tags.append(tag)

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
    
    def test_view_tags(self):
        """View all tags"""
        with app.test_client() as client:
            resp = client.get(f'/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
    
    def test_view_tag_details(self):
        """View tag details"""
        with app.test_client() as client:

            resp = client.get(f'/tags/{self.tag_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)

    def test_add_tag(self):
        """Add new tag"""
        with app.test_client() as client:
            d = {"tag-name" : "TestTag2"}
            resp = client.post('/tags/new', data = d, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)
            self.assertIn('TestTag2', html)

    def test_delete_tag(self):
        """Delete tag"""
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul>\n    \n</ul>', html)