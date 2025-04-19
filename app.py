from flask import Flask , render_template , redirect , url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'mysecretkey'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    employees = db.Column(db.Integer, nullable=False)

class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    employees = StringField('Employees', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home_page():
    return render_template('HomePage.html')

@app.route('/companys')
def companys_list():
    companys = Company.query.all()
    return render_template('CompanysList.html', companys=companys)

@app.route('/companys/new', methods=['GET', 'POST'])
def new_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            employees=form.employees.data
        )
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('companys_list'))
    return render_template('CompanyForm.html', form=form)

@app.route('/companys/<int:id>' , methods=['GET'])
def company_details(id):
    company = Company.query.get(id)
    return render_template('CompanyDetails.html', company=company)