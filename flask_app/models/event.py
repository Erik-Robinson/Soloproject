from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Event:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.with_users = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO events (name, date, location, description, user_id) VALUES (%(name)s, %(date)s, %(location)s,%(description)s, %(user_id)s);"
        return connectToMySQL('project').query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL('project').query_db(query,data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        event =  cls(results[0])
        return event
    
    @classmethod
    def update(cls,data):
        query = "UPDATE events SET name = %(name)s, date = %(date)s, location = %(location)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL('project').query_db(query, data)

    @classmethod
    def get_one_with_creator(cls,data):
        query = "SELECT * FROM events JOIN users ON events.user_id = users.id WHERE events.id = %(id)s;"
        results = connectToMySQL('project').query_db(query,data)
        event =  cls(results[0])
        user_data = {
                'id': results[0]['users.id'],
                'username': results[0]['username'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['created_at'],
                'updated_at': results[0]['updated_at']                 
        }
        creator = user.User(user_data)
        event.creator = creator
        return event

    @classmethod
    def get_all_with_creator(cls):
        query = "SELECT * FROM events JOIN users ON events.user_id = users.id ORDER BY date ASC;"
        results = connectToMySQL('project').query_db(query)
        all_events = []
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
            single_event = cls(event_data)
            user_data = {
                'id': one_event['users.id'],
                'username': one_event['username'],
                'email': one_event['email'],
                'password': one_event['password'],
                'created_at': one_event['created_at'],
                'updated_at': one_event['updated_at']                
            }
            single_user = user.User(user_data)
            single_event.creator = single_user
            all_events.append(single_event)
        return all_events
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        results = connectToMySQL('project').query_db(query)
        all_events = []
        for row in results:
            all_events.append( cls(row) )
        return all_events
    
    @classmethod
    def get_event_with_users(cls, data):
        query = "SELECT * FROM events LEFT JOIN rsvp ON rsvp.event_id = events.id LEFT JOIN users on rsvp.user_id = users.id WHERE events.id = %(id)s;"
        results = connectToMySQL('project').query_db(query)
        event =  cls(results[0])
        for results in results:
            user_data = {
                    'id': results[0]['users.id'],
                    'username': results[0]['username'],
                    'email': results[0]['email'],
                    'password': results[0]['password'],
                    'created_at': results[0]['created_at'],
                    'updated_at': results[0]['updated_at']                 
        }
        event.with_users.append( user.User( user_data) )
        return event
    
    @classmethod
    def add_rsvp(cls, data):
        query = "INSERT into rsvp (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        return connectToMySQL('project').query_db(query,data)
    
    @classmethod
    def grab_rsvp(cls, data):
        query = "SELECT COUNT(*) COUNT FROM rsvp WHERE event_id = %(id)s;"
        return connectToMySQL('project').query_db(query, data)

    
    @staticmethod
    def validate_event(event):
        is_valid = True
        if len(event['name']) < 2:
            is_valid = False
            flash('Event name must be entered!', "event")
        if len(event['location']) < 5:
            is_valid = False
            flash('location must be entered!', "event")
        if len(event['description']) < 10:
            is_valid = False
            flash('description must be entered!', "painting")
        return is_valid