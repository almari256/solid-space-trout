import os

from upload import upload
from process import process
from base_utils import base_utils
from datetime import datetime
from agents import agents

from flask import Flask , render_template , request , redirect , url_for , session , flash , jsonify

os.environ['OPENAI_API_KEY'] = 'sk-proj-b0Tz4zaPH4NMEBrmUY2HT3BlbkFJKxfrLIEQJuhqojdF2Im2'

def log_login_attempt(username , success) : 

    with open('loginlogs.txt' , 'a') as f : 

        log_entry = f"{datetime.now()} - {'Success' if success else 'Failure'} - User: {username}\n"
        f.write(log_entry)

app = Flask(__name__)
app.secret_key = 'lohitchat'
open('chat_logs.json' , 'w').write('')

# Static user credentials
users = {
    'user1@gmail.com': 'user1@123',
    'user2@gmail.com': 'user2@123'
}


@app.route('/')
def home() : return redirect(url_for('login'))


@app.route('/login' , methods = ['GET' , 'POST'])
def login() : 

    if request.method == 'POST' : 

        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password : 

            session['username'] = username
            log_login_attempt(username , True)

            return redirect(url_for('dashboard'))

        else : 
       
            log_login_attempt(username , False)
            flash('Invalid username or password')

    return render_template('login.html')


# @app.route('/')
# def index(): return render_template('temp_3.html')

@app.route('/dashboard')
def dashboard() : 

    if 'username' in session : 

        # return render_template('dashboard.html', username=session['username'])
        return render_template('temp_3.html' , username = session['username'])

    else : return redirect(url_for('login'))


@app.route('/upload')
def upload_page() : return render_template('admin.html')


@app.route('/api/feedback' , methods = ['POST'])
def feedback() : 

    data = request.json

    base_utils.write_to_log(data)

    return jsonify({'status': 'Feedback received'})


@app.route('/api/chatbot' , methods = ['POST'])
def chatbot() : 

    data = request.get_json()

    bot_response = {'text' : agents.run_agent(data)}

    return jsonify(response=bot_response)


@app.route('/api/upload' , methods = ['POST'])
def upload_file() : 

    file = request.files

    if 'file' not in file: return jsonify({'error': 'No file part in the request'}), 400

    file = file['file']

    response = upload.upload(file)

    return response


@app.route('/api/process' , methods = ['POST'])
def process_file() : 

    response = process.process()

    return jsonify({'message': 'Processing completed successfully.'}), 200


@app.route('/logout')
def logout() : 

    session.pop('username' , None)

    return redirect(url_for('login'))


# if __name__ == '__main__' : app.run(host = '0.0.0.0', port = 5000 , debug = True , use_reloader = False)
if __name__ == '__main__' : app.run(host = '0.0.0.0', port = 5000 , debug = True , use_reloader = True)