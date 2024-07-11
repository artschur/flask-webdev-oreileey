import flask
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

db = []

class User:
    def __init__(self, email, passw):
        self.email = email
        self.passw = passw

    

class Login(FlaskForm):
    email = EmailField('Insert your name: ', validators=[DataRequired()])
    password = PasswordField('Insert your password: ', validators=[DataRequired()])
    date = DateField('InsetDate',validators=[DataRequired()])
    submit = SubmitField('Submit')

app = flask.Flask(__name__) #__name__ determina o local da aplicacao, para achar templates, imagens a partir do path
app.config['SECRET_KEY'] = 'htg'

@app.route("/", methods=['GET', 'POST'])
def index():
    return flask.render_template("login.html")



@app.route('/name', methods=['POST', 'GET'])
def name():
    form = Login()
    # if flask.request.method == 'POST': #works
    #     return flask.redirect('/useragent')
    if form.validate_on_submit(): #IS MORE SPECIFIC,  focuses on the form
        db.append(User(form.email.data, form.password.data))
        if form.email.data != 'arth@gmail.com':
            flask.flash('stop baby!')
        flask.session['email'] = form.email.data #after i redirect there willl be no more name
        print(form.email.data)
        print(form.date.data)
        return flask.redirect('/name')
    return flask.render_template('name.html', form=Login())

@app.route('/dynamic/<name>', methods=['POST', 'GET']) #dynamic routes
def user(name):
    return flask.render_template('user.html', name=name)

@app.errorhandler(404)
def pageNotFound(e):
    return flask.render_template('404.html'), 404

@app.route('/useragent', methods=['GET'])
def agent():
    userAgent = flask.request.headers.get('User-Agent')
    return f'{userAgent}'

@app.route('/users', methods=['GET','POST'])
def returnUsers():
    return [{i.email: i.passw} for i in db]


if __name__ == "__main__":  #se o arquivo for executado diretamente, ele vai rodar o app
    app.run(debug=True) #debug=True, para atualizar a pagina automaticamente