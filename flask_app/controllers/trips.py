from flask_app import app
from flask import render_template,redirect,request,session,flash,jsonify
from flask_app.models.trip import Trip
from flask_app.models.user import User
from datetime import datetime

# new trip
@app.route('/trip/new')
def new_trip():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id':session['user_id']})   
    return render_template("new_trip.html",user=user) 

# trip create    
@app.route('/trip/create', methods=['POST'])
def create_trip():
    
    # validate the form here ...
    if not Trip.validate_trip(request.form):
        # redirect to trip creation 
        return redirect('/trip/new')
    # Call the save @classmethod on Trip
    Trip.save_trip(request.form)
    return redirect("/dashboard")

# trip delete
@app.route('/trip/delete/<int:trip_id>')
def delete_trip(trip_id):
    data = {'id':trip_id}
    Trip.delete_trip(data)
    return redirect("/dashboard")

# trip edit
@app.route('/trip/edit/<int:trip_id>')
def edit_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':trip_id}
    print('date',datetime.now())
    user=User.get_one({'id':session['user_id']})
    trip=Trip.get_one_trip(data)
    return render_template("edit_trip.html",trip=trip,user=user) 

# trip update
@app.route('/trip/update', methods=['POST'])
def trip_update():
    if not Trip.validate_trip(request.form):
        data = {'id':request.form['id']}

        user=User.get_one({'id':session['user_id']})
        trip=Trip.get_one_trip(data)
        # return to trip edit
        
        return render_template("edit_trip.html",trip=trip,user=user)
    
    print('request',request.form)    
    Trip.update_trip(request.form)
    return redirect("/dashboard")

# Join Trip
@app.route('/trip/join_trip', methods=['POST'])
def join_trip():
    data = request.form
    print("data",data)
    Trip.trip_join(data)
    return redirect("/dashboard")

# Cancel Trip
@app.route('/trip/cancel', methods=['POST'])
def cancel_trip():  
    data = request.form
    Trip.trip_cancel(data)
    return redirect("/dashboard")

# Show trip
@app.route('/trip/<int:trip_id>')
def show_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':trip_id}
    trip=Trip.get_one_trip(data)
    print('user id',trip.user_id)
    user = User.get_one({'id':session['user_id']})
    trip_user=User.get_one({'id':trip.user_id})
    data = {'trip_id':trip_id,'user_id':session['user_id']}
    users_trip=User.get_users_trip(data)
    print('users',users_trip)
    return render_template("show_trip.html",trip=trip,user=user,users_trip=users_trip,trip_user=trip_user) 


