import ssl
import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import certifi
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv

load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'


class UploadForm(FlaskForm):
    file = FileField('Upload CSV', validators=[DataRequired()])
    submit = SubmitField('Send Emails')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        send_emails(filepath)
        # delete the file after sending emails
        os.remove(filepath)
        flash('Emails sent successfully!', 'success')
        return redirect(url_for('upload_file'))
    return render_template('upload.html', form=form)


def send_emails(filepath):
    df = pd.read_csv(filepath)
    for index, row in df.iterrows():
        send_email(row['email'])


def send_email(to_email):

    html_content = render_template('email.html', name=to_email)
    message = Mail(
        from_email=os.environ.get("SENDGRID_FROM_EMAIL"),
        to_emails=to_email,
        subject='View your professional profile on Executor Exchange LLC',
        html_content=html_content)

    try:
        sg = SendGridAPIClient(
            api_key=os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f'Email sent to {to_email}: Status {response.status_code}')
    except Exception as e:
        print(f'Error sending email to {to_email}: {str(e)}')


if __name__ == '__main__':
    app.run(debug=True)
