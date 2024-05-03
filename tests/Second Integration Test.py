import unittest
from flask import Flask, url_for
from flask_testing import TestCase

# Import your Flask app here
from fitness_buddy_app import app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_page(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the fitness_buddy_app!', response.data)

if __name__ == '__main__':
    unittest.main()
