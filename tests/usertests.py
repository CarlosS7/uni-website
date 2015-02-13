import unittest
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
        assert b'are not authorized to view this page' in rv.data
        rv = self.app.get('/user/addexaminee', follow_redirects=True)
        assert b'are not authorized to view this page' in rv.data
        rv = self.app.get('/user/examscore', follow_redirects=True)
        assert b'are not authorized to view this page' in rv.data
        rv = self.app.get('/user/examwriting', follow_redirects=True)
        assert b'are not authorized to view this page' in rv.data

    def test_exam_pages(self):
        rv = self.app.get('/exam', follow_redirects=True)
        assert b'You are not authorized to view this page' in rv.data

class TestUser(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        self.user = User('admin', 'default', 'admin')
        db.session.add(self.user)
        db.session.commit()
        self.examinee = User('examinee', 'hard2guess', 'examinee', 'pyueng5')
        db.session.add(self.examinee)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        assert self.user.is_authenticated() is True
        assert self.user.role == 'admin'
        assert self.user.id == int(self.user.get_id())
        assert self.examinee.is_authenticated() is True
        assert self.examinee.role == 'examinee'
        assert self.examinee.exam_id == 'pyueng5'
        assert self.examinee.id == int(self.examinee.get_id())

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
        assert b'You have been logged in' in rv.data
        rv = self.logout()
        assert b'You have been logged out' in rv.data
        rv = self.login('adxmin', 'default')
        assert b'Invalid credentials' in rv.data
        rv = self.login('admin', 'dxefault')
        assert b'Invalid credentials' in rv.data

if __name__ == '__main__':
    unittest.main()
