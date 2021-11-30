import unittest
from app.models import User, Post, Follow


class FlaskClientTestCase(unittest.TestCase):

    def test_User(self):
        u = User()
        self.assertFalse(u.password_hash is not None)

    def test_Post(self):
        u = Post()
        self.assertFalse(u.timestamp is not None)

    def test_Follow(self):
        u = Follow()
        self.assertFalse(u.follower_id is not None)

    def test_Post_au(self):
        u = Post()
        self.assertFalse(u.author is not None)
