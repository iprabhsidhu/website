from flask import Flask, render_template, request, redirect, url_for, session,g
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import pytz
import re
import random
from passlib.hash import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify
from werkzeug.utils import secure_filename
from gridfs import GridFS

# import pymysql

app = Flask(__name__)

app.secret_key = 'xyz'
connection_string = 'mongodb+srv://hackers_co:K9mDEAed8NYtQeLd@blog.xk7q6yw.mongodb.net/'
client = MongoClient(connection_string)
db = client["webdb"]  # Update with your MongoDB database name
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comment"]
logs_collection = db['logs']
@app.route('/admin')
def admin():
    # Ensure only admin has access
    # Fetch all posts from the database
    posts = posts_collection.find()
    return render_template('admin_Panel.html', posts=posts)


@app.route('/admin/delete_post/<post_id>', methods=['POST'])
def admin_delete_post(post_id):
    posts_collection.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('admin'))

@app.route('/admin/logs', methods=['GET', 'POST'])
def admin_logs():
    if request.method == 'POST':
        log_type = request.form.get('log_type')
      

        if log_type == 'registration':
            # Fetch registration logs (if available)
            registration_logs = logs_collection.find({'log_type': 'registration'})
            
            return render_template('admin_logs.html', log_type='Registration Logs', logs=registration_logs)
        elif log_type == 'posting':
            # Fetch posting logs (if available)
            posting_logs = logs_collection.find({'log_type': 'posting'})
            return render_template('admin_logs.html', log_type='Posting Logs', logs=posting_logs)
        elif log_type == 'comments':
            # Fetch comments logs (if available)
            comments_logs = logs_collection.find({'log_type': 'comments'})
            return render_template('admin_logs.html', log_type='Comments Logs', logs=comments_logs)

    return render_template('admin_logs.html')


@app.route('/admin/user_list')
def admin_user_list():
    # Fetch all users from the database
    all_users = users_collection.find()
    return render_template('admin_user_list.html', users=all_users)

# Route to perform admin actions (ban or warn) on users
@app.route('/admin/user_action/<user_id>/<action>', methods=['GET', 'POST'])
def admin_user_action(user_id, action):
    if action == 'ban':
        # Implement user ban functionality
        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': 'banned'}})
    elif action == 'warn':
        if request.method == 'POST':
            warn_message = request.form.get('warn_message')
            # Update the user's status to 'warned' and save the warning message
            users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': 'warned', 'warn_message': warn_message}})
            return redirect(url_for('admin_user_list'))
    elif action == 'unban':
        # Implement user unban functionality
        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': 'active'}})
    
    return redirect(url_for('admin_user_list'))
if __name__=="__main__":
    from waitress import serve
    app.run(debug=True)

