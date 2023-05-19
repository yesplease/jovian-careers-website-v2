import os
from flask_xcaptcha import XCaptcha

my_secret = os.environ['DB_CONNECTION_STRING']
captcha_secret = os.environ['CAPTCHA_SECRET']
chaptcha_site_key = 'da3aea6f-769c-4cdd-ac6d-6d7764548249'
from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_df

app = Flask(__name__)
app.config['XCAPTCHA_SITE_KEY'] = chaptcha_site_key
app.config['XCAPTCHA_SECRET_KEY'] = captcha_secret
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"
xcaptcha = XCaptcha(app=app)

@app.route("/")
def hello_jovian():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id):
  print('this is ID in app.route /job/<id>')
  print(id)
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html',
                        job=job)

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  job = load_job_from_db(id)
  data = request.form

  #server-side validation of captcha
  if xcaptcha.verify():
    return render_template('application_submitted.html',
                        application=data,
                        job=job)
  else:
    return render_template('captcha_error.html',
                        application=data)
  
  #store in db
  add_application_to_df(id, data)
  



@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
