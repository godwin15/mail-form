import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
import configparser
import re
import traceback


app = Flask(__name__, template_folder="templates/", static_url_path="/static")
app.secret_key = os.urandom(16)

config = configparser.ConfigParser()
config.read('.env')

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config['ENV']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['ENV']['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = config['ENV']['MAIL_USERNAME']

mail = Mail(app)

#validating the format of the email if needed
def validate_email(email):
    #validation logic
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process_email', methods=['POST'])
def process_email():
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')

    if validate_email(email):
        try:
            # Send the email using Flask-Mail
            msg = Message("New Subscription", recipients=["godwinsilayo100@gmail.com"])
            msg.body = f"{firstName} {lastName} with Emaail: {email} has joined our mailing list \n\n Thank you"
            mail.send(msg)
            flash("Thank you for subscribing! We have sent you a confirmation email.")
            return redirect(url_for('home')) 
        except Exception as e:
            print("Error sending email:", e)
            traceback.print_exc()
            flash("Oops! Something went wrong. Please try again later.")
            return redirect(url_for('home')) 
    else:
        flash("Invalid email address. Please provide a valid email.")
        return redirect(url_for('home')) 


if __name__ == '__main__':
    app.run(debug=True)
