from flask import Flask, render_template, url_for, request, redirect
from pathlib import Path
import csv

app = Flask(__name__)
if not Path('./output/').exists():
    Path('./output/').mkdir()
output = Path('./output/messages.txt')
csv_output = Path('./output/database.csv')

@app.route("/")
def get_home():
    return render_template('/index.html')

@app.route("/<string:page_name>")
def html(page_name):
    return render_template(page_name)

def write_to_file(data):
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    with open(output, mode='a') as file:
        file.write(f"\n---------------------------------------------------------------------------------\n"
                   f"Email:{email}\n"
                   f"Subject:{subject}\n"
                   f"Message:{message}\n")

def write_to_csv(data):
    with open(csv_output, mode='a', newline='') as file:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thanks.html')
        except:
            return 'did not save to database'
    else:
        return 'Something went wrong. Try again!'