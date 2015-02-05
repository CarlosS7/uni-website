import os
import json
import unittest
from website import app, db
from website.models import User, Questions

class TestExaminee(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        self.examinee = User('examinee', 'hard2guess', 'examinee', 'silly1')
        db.session.add(self.examinee)
        db.session.commit()
        self.add_questions(self)

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.login('examinee', 'hard2guess')

    def tearDown(self):
        self.logout()

    def add_questions(self):
        with open(os.path.join('tests', 'testdata', 'exams', 'silly1.json')) as questions:
            pages = json.load(questions)
        with open(os.path.join('tests', 'testdata', 'exams', 'silly1_answers.json')) as answers:
            correct = json.load(answers)
        db.session.add(Questions('silly1', pages, correct))
        db.session.commit()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/user/logout', follow_redirects=True)

    def test_initial(self):
        rv = self.app.get('/exam', follow_redirects=True)
        assert b'read the instructions for each section carefully' in rv.data
        assert b'Ontologically the goal exists only in the imagination' in rv.data
        assert b'fart in your general direction' in rv.data
        assert b'a swallow bring a coconut to such a temperate zone' in rv.data

    def test_finish(self):
        rv = self.app.post('/exam/finish', follow_redirects=True)
        assert b'have been logged out' in rv.data

if __name__ == '__main__':
    unittest.main()
