import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Therapist, Booking

actor_token='Bearer ' + input()
actor_headers={'Authorization': actor_token}

class Test(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'a', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Example therapist for use in tests
        self.example_actor = {
            'name': 'shah'
        }


    
    def end(self):
        pass

    """
    Tests
    """

    def get_actor_success(self):
        res = self.client().get('/actors', headers=actor_headers)
        data = json.loads(res.data)

        # Check success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def get_actor_unauthenticated(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def delete_actor(self):
        res = self.client().delete('/actors/9999',headers=actor_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def add_actor(self):
        res = self.client().post('/actors', json="", headers=actor_headers, body={
            'name': 'test',
            'age': 30,
            'gender': 'M'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def update_actor(self):
        res = self.client().patch('/actors', json="", headers=actor_headers, body={
            'name': 'test',
            'age': 30,
            'gender': 'M'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()