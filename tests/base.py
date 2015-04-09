import unittest
import json
from website import app, db

class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/user/logout', follow_redirects=True)

    def add_examinee(self, username, exam_id, fullname):
        """Add examinee helper function."""
        return self.app.post('/user/addexaminee', data=json.dumps(dict(
            username=username,
            exam_id=exam_id,
            fullname=fullname
            )), content_type='application/json', follow_redirects=True)

