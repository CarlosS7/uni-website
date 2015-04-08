import unittest
import json
from website import app, db
from website.models import User

class TestUnauthorized(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_pages(self):
        rv = self.app.get('/user', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)
        rv = self.app.post('/user/addexaminee', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)
        rv = self.app.post('/user/examscore', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)

    def test_exam_pages(self):
        rv = self.app.get('/exam', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)

class TestUser(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        self.user = User(username='admin', role='admin')
        self.user.hash_password('default')
        db.session.add(self.user)
        db.session.commit()
        self.examinee = User(username='12345678', role='examinee',
                fullname='Charles Dickens', exam_id='silly1', answer_page='{}')
        self.examinee.hash_password('hard2guess')
        db.session.add(self.examinee)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(self.user.role, 'admin')
        self.assertEqual(self.user.id, int(self.user.get_id()))
        self.assertTrue(self.examinee.is_authenticated())
        self.assertEqual(self.examinee.role, 'examinee')
        self.assertEqual(self.examinee.exam_id, 'silly1')
        self.assertEqual(self.examinee.id, int(self.examinee.get_id()))

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/user/logout', follow_redirects=True)

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login('admin', 'default')
        self.assertIn(b'Students interested in courses', rv.data)
        rv = self.logout()
        self.assertIn(b'You have been logged out', rv.data)
        rv = self.login('adxmin', 'default')
        self.assertIn(b'Invalid credentials', rv.data)
        rv = self.login('admin', 'dxefault')
        self.assertIn(b'Invalid credentials', rv.data)

    def add_examinee(self, username, exam_id, fullname):
        """Add examinee helper function."""
        return self.app.post('/user/addexaminee', data=json.dumps(dict(
            username=username,
            exam_id=exam_id,
            fullname=fullname
            )), content_type='application/json', follow_redirects=True)

    def test_add_examinee(self):
        self.login('admin', 'default')
        rv = self.add_examinee('', 'silly1', 'Henry James')
        self.assertIn(b'Hide student names', rv.data)
        rv = self.add_examinee('12345678', 'silly1', 'Thomas Hardy')
        self.assertIn(b'12345678', rv.data)

if __name__ == '__main__':
    unittest.main()
