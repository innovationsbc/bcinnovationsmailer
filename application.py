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
def hello():
  r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                        data = {'secret' :
                                envs['RECAPTCHA_SECRET_KEY'],
                                'response' :
                                request.form['g-recaptcha-response']})

  google_response = json.loads(r.text)

  if google_response["success"]:

    requests.post("https://api.mailgun.net/v3/mg.billcookecreative.com/messages",
                  auth=("api", envs['MAILGUN_KEY']),
                  data={"from": "Bill Cooke Creative <donotreply@mg.billcookecreative.com>",
                        "to": [request.form['email']],
                        "bcc": ["nolan@bcinnovationsonline.com"],
                        "subject": "Contact Submitted",
                        "text": "Testing some Mailgun awesomness!"})

    success_message = {'message': 'success'}
    return jsonify(success_message)
  else:
    error_message = {'message': 'Please verify you are not a robot'}
    return jsonify(error_message), 401


if __name__ == "__main__":
    application.run(host='0.0.0.0')
