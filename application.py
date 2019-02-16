import requests, jsonify, json
from flask import Flask
from flask import request
from flask import jsonify
from flask_recaptcha import ReCaptcha

envfile = open(".envs")
envs = {}
for line in envfile:
  linesplit = line.split(':')
  try:
    envs.update({linesplit[0].strip(): linesplit[1].strip()})
  except:
    pass

application = Flask(__name__)

application.config.update({'RECAPTCHA_ENABLED': True,
                           'RECAPTCHA_SITE_KEY': envs['RECAPTCHA_SITE_KEY'],
                           'RECAPTCHA_SECRET_KEY': envs['RECAPTCHA_SECRET_KEY']})

recaptcha = ReCaptcha(app=application)

@application.route("/contact", methods = ['POST'])
def contact():
  # recaptcha validation
  r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                        data = {'secret' :
                                envs['RECAPTCHA_SECRET_KEY'],
                                'response' :
                                request.form['g-recaptcha-response']})

  google_response = json.loads(r.text)

  if google_response["success"]:

    if 'billcookecreative.com' in request.url_root:
      return billcookecreative_contact(request.form)
    else:
      error_message = {'message': 'Invalid post from client'}
      return jsonify(error_message), 401

  else:
    error_message = {'message': 'Please verify you are not a robot'}
    return jsonify(error_message), 401



def billcookecreative_contact(form):

  try:
    with open(str(envs['PATH_EMAIL_HTML']) + '/minwelcome.html', 'r') as html_file:
      html_string = html_file.read().replace('\n', '')

    html_string = html_string.replace('[NAME]', form['name'])

    requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                  auth=("api", envs['MAILGUN_KEY']),
                  files=[("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/bcc.png","rb")),
                         ("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/facebookicon.png","rb")),
                         ("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/instagramicon.png","rb"))],
                  data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                        "to": [form['email']],
                        "bcc": ["nolan@bcinnovationsonline.com"],
                        "subject": "Contact Sent",
                        "text": "Thanks for contacting. We will be in contact.\r\nBill Cooke",
                        "html": html_string})


    with open(str(envs['PATH_EMAIL_HTML']) + '/minhello.html', 'r') as html_file:
      html_string = html_file.read().replace('\n', '')

    html_string = html_string.replace('[NAME]', form['name'])
    html_string = html_string.replace('[CONTACTEMAIL]', form['email'])
    html_string = html_string.replace('[MESSAGEMESSAGE]', form['message'])
    html_string = html_string.replace('[SUBJECT]', form['subject'])
    text_string = str(form['name']) + ' has contacted you. ' + str(form['email']) + '\r\n\r\n' + str(form['subject']) + '\r\n\r\n' + str(form['message'])

    requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                  auth=("api", envs['MAILGUN_KEY']),
                  files=[("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/bcc.png","rb")),
                         ("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/facebookicon.png","rb")),
                         ("inline", open(str(envs['PATH_EMAIL_HTML']) + "/images/instagramicon.png","rb"))],
                  data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                        "to": [envs['BILLCOOKE_EMAIL']],
                        "bcc": ["nolan@bcinnovationsonline.com"],
                        "subject": form['subject'],
                        "text": text_string,
                        "html": html_string})


    success_message = {'message': 'success'}
    return jsonify(success_message)

  except:
    error_message = {'message': 'Error sending email contact'}
    return jsonify(error_message), 401

'''
@application.route("/localhost", methods = ['GET'])
def localhost_contact():

  form = {'name': 'Nolan Burfield',
          'email': 'nburf@nevada.unr.edu',
          'subject': 'Email Subject',
          'message': 'This is a message'}

  with open(str(envs['PATH_EMAIL_HTML']) + '/minwelcome.html', 'r') as html_file:
    html_string = html_file.read().replace('\n', '')

  html_string = html_string.replace('[NAME]', form['name'])

  requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                auth=("api", envs['MAILGUN_KEY']),
                files=[("inline", open("/home/nburfield/Development/billcookecreative/email/images/bcc.png","rb")),
                       ("inline", open("/home/nburfield/Development/billcookecreative/email/images/facebookicon.png","rb")),
                       ("inline", open("/home/nburfield/Development/billcookecreative/email/images/instagramicon.png","rb"))],
                data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                      "to": [form['email']],
                      "bcc": ["nolan@bcinnovationsonline.com"],
                      "subject": "Contact Sent",
                      "text": "Thanks for contacting. We will be in contact.\r\nBill Cooke",
                      "html": html_string})


  with open(str(envs['PATH_EMAIL_HTML']) + '/minhello.html', 'r') as html_file:
    html_string = html_file.read().replace('\n', '')

  html_string = html_string.replace('[NAME]', form['name'])
  html_string = html_string.replace('[CONTACTEMAIL]', form['email'])
  html_string = html_string.replace('[MESSAGEMESSAGE]', form['message'])
  html_string = html_string.replace('[SUBJECT]', form['subject'])
  text_string = str(form['name']) + ' has contacted you. ' + str(form['email']) + '\r\n\r\n' + str(form['subject']) + '\r\n\r\n' + str(form['message'])

  requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                auth=("api", envs['MAILGUN_KEY']),
                files=[("inline", open("/home/nburfield/Development/billcookecreative/email/images/bcc.png","rb")),
                       ("inline", open("/home/nburfield/Development/billcookecreative/email/images/facebookicon.png","rb")),
                       ("inline", open("/home/nburfield/Development/billcookecreative/email/images/instagramicon.png","rb"))],
                data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                      "to": [envs['BILLCOOKE_EMAIL']],
                      "bcc": ["nolan@bcinnovationsonline.com"],
                      "subject": form['subject'],
                      "text": text_string,
                      "html": html_string})


  success_message = {'message': 'success'}
  return jsonify(success_message)
'''


if __name__ == "__main__":
    application.run(host='0.0.0.0')
