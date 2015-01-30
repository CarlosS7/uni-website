import unittest
from website import app, db

class TestSignup(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def signup(self, username, email, phone):
        """Signup helper function"""
        return self.app.post('/signup', data=dict(
            username=username,
            email=email,
            phone=phone,
            coursename='IEP'
            ), follow_redirects=True)

    def test_valid_signup(self):
        rv = self.app.get('/signup', follow_redirects=True)
        assert b'Signing up for courses at ELEC' in rv.data
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        assert b'You have signed up for the' in rv.data
        assert b'Ideal for students who want to study a university course' in rv.data

    def test_repeat_signup(self):
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        assert b'seems like you have already signed up for the' in rv.data
        assert b'Ideal for students who want to study a university course' in rv.data

    def test_invalid_name(self):
        rv = self.signup('Char;lie Chaplin', 'charlie@chaplin.org', '832174261892')
        assert b'Name should only contain letters and spaces' in rv.data

    def test_invalid_email(self):
        rv = self.signup('Charlie Chaplin', 'charliechaplin.org', '832174261892')
        assert b'Invalid email address' in rv.data

    def test_invalid_phone(self):
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '8321742a61892')
        assert b'number can only contain numbers' in rv.data

if __name__ == '__main__':
    unittest.main()
