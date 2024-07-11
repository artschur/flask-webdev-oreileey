import flask
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'htgs'
class RegistrationForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('ready')

@app.route('/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flask.session['name']= form.username.data
        return flask.redirect('/name')
    return flask.render_template("book.html", form=form)

@app.route('/name', methods=['POST', 'GET'])
def sayHello():
    return flask.render_template('hello.html', name=flask.session['name'])


@app.route('/dynamic/')
def ok():
    name = flask.request.args.get('name')
    return f'Hello, {name}'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000,debug=True)