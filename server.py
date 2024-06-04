from flask import Flask, render_template, request
from smtplib import SMTP
from email.message import EmailMessage
import csv

app = Flask(__name__)

@app.route("/")
def root_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def home_page(page_name):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        if len(data) > 0:
            send_email(data)
            return render_template('thankyou.html', name=data.get('name'))
        else:
            return
    else: return 'Something went wrong. Try again'

def send_email(data):
    msg = EmailMessage()
    msg['From'] = data.get('email')
    msg['To'] = 'jamieabrahams123234@gmail.com'
    msg['Subject'] = data.get('subject')
    msg.set_content('From: ' + data.get('email') + '\n' + 'Message: ' + data.get('message'))
    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo() 
        smtp.starttls() 
        smtp.login('pythonemailserver.smtp@gmail.com','iyzo jopq octf ojad')
        smtp.send_message(msg)
        try:
            write_to_file(data)
            write_to_csv(data)
        except:
            return 'Did not save to database'
        smtp.quit()

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])