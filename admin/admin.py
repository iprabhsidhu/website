
@app.route('/admin')
def admin():
    # Ensure only admin has access
    # Fetch all posts from the database
    posts = posts_collection.find()
    return render_template('admin_panel.html', posts=posts)


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


