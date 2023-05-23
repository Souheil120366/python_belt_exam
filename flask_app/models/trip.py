from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from datetime import datetime

class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.destination = data['destination']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.plan = data['plan']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    # validate tv show inputs 
    @staticmethod
    def validate_trip( trip ):
        current_date = datetime.now().date()
        print('im here',trip)
        print('start date',trip['start_date']) 
        is_valid = True
        start_date = datetime.strptime(trip['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(trip['end_date'], "%Y-%m-%d").date()
        # test whether a field matches the pattern
        if len(trip['destination']) < 3:
            flash("Destination must be at least 3 characters!","trip")
            is_valid = False
        if len(trip['start_date']) < 1:
            flash("Invalid Start Date !","trip")
            is_valid = False 
        elif (start_date < current_date):
            flash("Invalid Start Date !","trip")
            is_valid = False
        if len(trip['end_date']) < 1:
            flash("Start Date should be after current date !","trip")
            is_valid = False    
        elif (end_date < start_date):
            flash("End Date less than Start Date !","trip")
            is_valid = False
        if len(trip['plan']) < 3:
            flash("Plan must be at least 3 characters!","trip")
            is_valid = False
        return is_valid
    
    # get all trips created and joined by logged user
    @classmethod
    def get_all_user_trips(cls,data):
        query = "SELECT * FROM trips left join join_trip on trips.id=join_trip.trip_id where (join_trip.user_id=%(id)s or trips.user_id=%(id)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    # get all trips not joined by logged user
    @classmethod
    def get_all_trips(cls,data):
        query = "SELECT * FROM trips left join join_trip on trips.id=join_trip.trip_id where ((join_trip.user_id != %(id)s or join_trip.user_id is null) and trips.user_id != %(id)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    # get one trip by id
    @classmethod
    def get_one_trip(cls,data):
        query = "SELECT * FROM trips WHERE id=%(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
           return cls(result[0])
        return result
       
    # create trip    
    @classmethod
    def save_trip(cls, data ):
        print('req',data)
        query = "INSERT INTO trips ( destination, start_date, end_date, plan, user_id, created_at, updated_at ) VALUES ( %(destination)s, %(start_date)s, %(end_date)s ,%(plan)s, %(user_id)s, NOW(), NOW() );"
        return connectToMySQL(DATABASE).query_db( query, data )        

    # delete trip
    @classmethod
    def delete_trip(cls,data):
        query="DELETE FROM join_trip WHERE trip_id =  %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        query="DELETE FROM trips WHERE trips.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    # update trip
    @classmethod
    def update_trip(cls,data):
        query = "update trips set destination=%(destination)s, start_date=%(start_date)s, end_date=%(end_date)s, plan=%(plan)s where id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    # create join table
    @classmethod
    def trip_join(cls,data):
        query = "INSERT INTO join_trip (user_id, trip_id) SELECT %(user_id)s, %(trip_id)s WHERE NOT EXISTS (SELECT * FROM join_trip WHERE user_id =%(user_id)s  and trip_id=%(trip_id)s );"
        results = connectToMySQL(DATABASE).query_db(query,data)
          
        return results
    
    # if cancel delete row id=trip_id from join table
    @classmethod
    def trip_cancel(cls,data):
        query = "delete from join_trip where (user_id = %(user_id)s and trip_id = %(trip_id)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results
    
    # select all user joined trip
    @classmethod
    def get_all_user_join(cls,data):
        query = "SELECT * FROM join_trip where user_id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        join_list=[]
        for join in results:
            join_list.append(join['trip_id'])
        return join_list
