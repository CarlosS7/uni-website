import os
import json
import unittest
from website import app, db
from website.models import User, Questions
from website.scripts import get_score, calc_score

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
        """Login helper function."""
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Logout helper function."""
        return self.app.get('/user/logout', follow_redirects=True)

    def mock_test(self, ans1, ans2, ans3, ans4, ans5):
        """Take test helper function."""
        return self.app.post('/exam/finish', data={
            'silly1_list_01': ans1,
            'silly1_list_02': ans2,
            'silly1_struct_03': ans3,
            'silly1_struct_04': ans4,
            'silly1_read_05': ans5 
            }, follow_redirects=True)

    def test_initial(self):
        rv = self.app.get('/exam', follow_redirects=True)
        self.assertIn(b'read the instructions for each section carefully', rv.data)
        self.assertIn(b'Ontologically the goal exists only in the imagination', rv.data)
        self.assertIn(b'fart in your general direction', rv.data)
        self.assertIn(b'a swallow bring a coconut to such a temperate zone', rv.data)

    def test_full(self):
        self.mock_test("B", "D", "D", "A", "C")
        user = User.query.filter_by(username='examinee').first()
        score = get_score(user)
        listening, structure, reading = calc_score(score)
        self.assertEqual(len(score), 5)
        self.assertEqual(listening, 2)
        self.assertEqual(structure, 2)
        self.assertEqual(reading, 1)

    def test_not_full(self):
        self.mock_test("B", "B", "D", "C", "C")
        user = User.query.filter_by(username='examinee').first()
        score = get_score(user)
        listening, structure, reading = calc_score(score)
        self.assertEqual(len(score), 3)
        self.assertEqual(listening, 1)
        self.assertEqual(structure, 1)
        self.assertEqual(reading, 1)

    def test_finish(self):
        rv = self.app.post('/exam/finish', follow_redirects=True)
        self.assertIn(b'have been logged out', rv.data)

if __name__ == '__main__':
    unittest.main()
