from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import event
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.events = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('project').query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL('project').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('project').query_db(query, data)
        if not results:
            return False
        return User(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        if not results:
            return False
        return User(results[0])
    
    @classmethod
    def get_user_with_events(cls, data):
        query = "SELECT * FROM users LEFT JOIN rsvp ON rsvp.user_id = users.id LEFT JOIN events on rsvp.event_id = events.id WHERE users.id = %(id)s;"
        results = connectToMySQL('project').query_db(query)
        user = cls( results[0])
        for one_event in results:
            event_data = {
                "id": one_event['id'],
                'name': one_event['name'],
                'date': one_event['date'],
                'location': one_event['location'],
                'description': one_event['description'],
                'created_at': one_event['created_at'],
                'updated_at': one_event['updated_at']
            }
            user.events.append( event.Event( event_data ) )
            return user
    
    @classmethod
    def add_rsvp(cls, data):
        query = "INSERT into rsvp (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        return connectToMySQL('project').query_db(query,data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('project').query_db(query,user)
        if results:
            flash("Email already in use.",'register')
            is_valid = False
        if len(user['username']) < 2:
            flash("Username must be at least 3 chracters!", 'register')
        if not EMAIL_REGEX.match(user['email']):
            flash("INVALID email address!", 'email')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!", 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords to not match!")
            is_valid = False
        return is_valid