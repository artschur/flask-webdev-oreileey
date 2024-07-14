import flask
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired
from db import db, User, Role  # Importing the db object and User model
from flask_migrate import Migrate



app = flask.Flask(__name__)  # __name__ determines the location of the application, for finding templates, images from the path
app.config['SECRET_KEY'] = 'htg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the database with the app


@app.shell_context_processor #when i run flask shell this will be added
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Role':Role}

migrate = Migrate(app, db)

class Login(FlaskForm):
    email = EmailField('Insert your email: ', validators=[DataRequired()])
    password = PasswordField('Insert your password: ', validators=[DataRequired()])
    role  = SelectField('Role', choices=[(1, 'User'), (2, 'Admin')], coerce=int)
    submit = SubmitField('Submit')


@app.route("/", methods=['GET', 'POST'])
def index():
    return flask.render_template("login.html")

@app.route('/add/user', methods=['POST', 'GET'])
def name():
    form = Login()
    if form.validate_on_submit():
        user = User(username=form.email.data, password=form.password.data, role_id=form.role.data)  # Assuming a default role_id for now. Creates a user obj and adds to table
        db.session.add(user)
        db.session.commit()
        flask.session['email'] = form.email.data
        return flask.redirect('/add/user')
    return flask.render_template('name.html', form=form)

@app.route('/dynamic/<name>', methods=['POST', 'GET'])  # dynamic routes
def user(name):
    return flask.render_template('user.html', name=name)

@app.errorhandler(404)
def pageNotFound(e):
    return flask.render_template('404.html'), 404

@app.route('/useragent', methods=['GET'])
def agent():
    userAgent = flask.request.headers.get('User-Agent')
    return f'{userAgent}'

@app.route('/users', methods=['GET', 'POST'])
def returnUsers():
    users = User.query.all()
    return [{user.username: user.password} for user in users]

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)  # debug=True, to auto-reload the page
