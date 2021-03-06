import numbers
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethingsecure'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup_form():
    return render_template('signup.html')


@app.route('/report')
def check_username():
    lower_letter = False
    upper_letter = False
    num_end = False
    username = request.args.get('username')
    lower_letter = any(c.islower()
                       for c in username)  # check if any of this is true
    upper_letter = any(c.isupper()
                       for c in username)
    num_end = username[-1].isdigit()
    report = lower_letter and upper_letter and num_end
    return render_template('report.html', report=report, lower=lower_letter, upper=upper_letter, num_end=num_end)


@app.route('/thankyou')
def thank_you():
    first = request.args.get('first')  # grab user info from the form input
    last = request.args.get('last')
    return render_template('thankyou.html', first=first, last=last)


class InfoForm(FlaskForm):
    breed = StringField('What event you\'re looking for?')
    submit = SubmitField('Submit')


@app.route('/form', methods=['GET', 'POST'])
def get_form():
    breed = False
    form = InfoForm()
    if form.validate_on_submit():
        breed = form.breed.data
        form.breed.data = ''
    return render_template('form.html', form=form, breed=breed)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
