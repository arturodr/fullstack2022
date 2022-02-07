import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_user = os.getenv('DB_USER')
        self.database_pass = os.getenv('DB_PASS')
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.database_user, self.database_pass, 'localhost:5432',
                                                               self.database_name)
        setup_db(self.app, self.database_path)

        self.test_question = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'difficulty': 1,
            'category': '1'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_create_question(self):

        questions_before_insert = Question.total_questions()

        response = self.client().post('/questions', json=self.test_question)
        data = json.loads(response.data)

        questions_after_insert = Question.total_questions()

        self.assertTrue(questions_after_insert-questions_before_insert == 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_404(self):

        questions_before_insert = Question.total_questions()

        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        questions_after_insert = Question.total_questions()

        self.assertTrue(questions_after_insert-questions_before_insert == 0)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)

    def test_delete_questions(self):
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 15)

    def test_delete_questions_404(self):
        res = self.client().delete('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)

    def test_delete_questions_404_out_off_range(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)

    def test_search_questions(self):
        json_data = {
            'searchTerm': '1990'
        }
        res = self.client().post('/questions/search', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_questions_422(self):
        json_data = {
            'searchTerm': ''
        }
        res = self.client().post('/questions/search', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)

    def test_get_questions_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_play(self):
        json_data = {
            'previous_questions': [],
            'quiz_category': {"type": "Science", "id": "1"},
        }
        res = self.client().post('/quizzes', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_play_422(self):
        json_data = {}
        res = self.client().post('/quizzes', json=json_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
