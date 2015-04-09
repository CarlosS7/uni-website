import unittest
from .base import BaseCase

class TestSignup(BaseCase):
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
        self.assertIn(b'Signing up for courses at ELEC', rv.data)
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        self.assertIn(b'You have signed up for the', rv.data)
        self.assertIn(b'Ideal for students who want to study a university course', rv.data)

    def test_repeat_signup(self):
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '832174261892')
        self.assertIn(b'seems like you have already signed up for the', rv.data)
        self.assertIn(b'Ideal for students who want to study a university course', rv.data)

    def test_invalid_name(self):
        rv = self.signup('Char;lie Chaplin', 'charlie@chaplin.org', '832174261892')
        self.assertIn(b'Name should only contain letters and spaces', rv.data)

    def test_invalid_email(self):
        rv = self.signup('Charlie Chaplin', 'charliechaplin.org', '832174261892')
        self.assertIn(b'Invalid email address', rv.data)

    def test_invalid_phone(self):
        rv = self.signup('Charlie Chaplin', 'charlie@chaplin.org', '8321742a61892')
        self.assertIn(b'number can only contain numbers', rv.data)

if __name__ == '__main__':
    unittest.main()
