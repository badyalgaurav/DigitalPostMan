# from flask import Flask
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from flask import Flask, render_template, request, make_response, jsonify
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filepath=os.path.join("attachments", secure_filename(f.filename));
      f.save(filepath)

      resp = make_response(filepath)
      resp.status_code = 200
      resp.headers['Access-Control-Allow-Origin'] = '*'
      return resp

'''
reference
https://stackoverflow.com/questions/882712/sending-html-email-using-python
Note: need to change the line from sample code from reference
 mail.sendmail(email, To, msg.as_string())'''
@app.route('/email_sender')
def email_sender():
    email=str(request.args.get('login_email'));
    pwd=str(request.args.get('login_pwd'));

    receiver_emails=str(request.args.get('receiver_emails'));
    receiver_emails_array = [x.strip() for x in receiver_emails.split(',')]
    email_body=str(request.args.get('email_content'));

    email_header=str(request.args.get('email_header'));

    attachment_path= str(request.args.get('attachment_path'));
    attachment = open(attachment_path, "rb")
    filename = os.path.basename(attachment_path)
    for receiver_email in receiver_emails_array:

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_header
        msg['From'] = email
        msg['To'] = receiver_email
        msg.add_header('Content-Type', 'text/html')
        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = email_body
        # Record the MIME types of both parts - text/plain and text/html.
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        # msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login(email,pwd)
        mail.sendmail(email, receiver_email, msg.as_string())
        mail.quit()

        #this code is used for removing the element from error to avoid to send mail again
        # receiver_emails_array.remove(receiver_email)



    resp =make_response("success")
    # resp.set_cookie("login_user_name", value=response[0]["username"])
    # resp.set_cookie("user_id", value=response[0]["user_id"])



    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run()
