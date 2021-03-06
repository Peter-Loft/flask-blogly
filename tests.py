from unittest import TestCase

from app import app, db
from models import User, Post

# Let's configure our app to use a different database for tests
app.config["DATABASE_URL"] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first", last_name="test_last", image_url=""
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url="",
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        whisky_post = Post(
            title="Whiskeys Opinions",
            content="I have none.",
            user_id=second_user.id
        )

        db.session.add(whisky_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post = whisky_post

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_users_list(self):
        """Test users list page"""

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_user_form(self):
        """Test add user form page"""

        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Add User Page Verficiation", html)

    def test_add_user(self):
        """Test add user submission"""

        with self.client as c:
            resp = c.post(
                "/users/new",
                data={"fname": "SPIKE", "lname": "PORCUPINE", "image_url": ""},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(" Users list, homepage ", html)

            new_user = User.query.filter(User.first_name == "SPIKE").first()
            self.assertEqual(new_user.first_name, "SPIKE")
            self.assertEqual(new_user.last_name, "PORCUPINE")
            self.assertEqual(new_user.image_url, "")

    def test_edit_user(self):
        """Test edit user submission"""

        with self.client as c:
            resp = c.post(
                f"/users/{self.user_id}/edit",
                data={"fname": "SPIKE", "lname": "PORCUPINE", "image_url": ""},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(" Users list, homepage ", html)

            edited_user = User.query.filter(User.id == self.user_id).first()
            self.assertEqual(edited_user.first_name, "SPIKE")
            self.assertEqual(edited_user.last_name, "PORCUPINE")
            self.assertEqual(edited_user.image_url, "")

    def test_delete(self):
        """Test delete user route"""

        with self.client as c:
            resp = c.post(
                f"/users/{self.user_id}/delete", follow_redirects=True
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(" Users list, homepage ", html)

            found_users = User.query.filter(User.id == self.user_id).all()
            self.assertAlmostEqual(len(found_users), 0)

    def test_delete_invalid_id(self):
        """Test delete invalid user"""

        with self.client as c:
            resp = c.post(f"/users/222222/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(" Users list, homepage ", html)

# ============================================================
# POST TESTS
# ============================================================

    def test_post_details(self):
        """Test display of post details"""

        with self.client as c:
            resp = c.get(f"/posts/{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post detail page verification", html)
            self.assertIn(self.post.title, html)
            self.assertIn(self.post.content, html)

    def test_post_edit(self):
        """ Test logic to edit post"""

        with self.client as c:
            resp = c.post(f"/posts/{self.post.id}/edit",
                          data={
                              "title": "Hello",
                              "content": "Big wide World",
                              "user_id": self.post.user_id
                          },
                          follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello", html)
            self.assertIn("Big wide World", html)

            edited_post = Post.query.filter(Post.id == self.post.id).first()
            self.assertEqual(edited_post.title, "Hello")
            self.assertEqual(edited_post.content, "Big wide World")