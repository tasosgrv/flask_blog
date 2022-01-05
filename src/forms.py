from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    username = StringField(label='Username', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                        Length(min=3, max=15, message="To username πρέπει να είναι απο 3-15 χαρακτηρες")]
                            )
    email = StringField(label='email', 
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")]
                        )
    password = PasswordField(label='password', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                        Length(min=3, max=15, message="To password πρέπει να είναι απο 3-15 χαρακτηρες")]
                            )
    password2 = PasswordField(label='Επιβεβαίωση password', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                        Length(min=3, max=15, message="To password πρέπει να είναι απο 3-15 χαρακτηρες"), 
                                        EqualTo('password', message="Τα δυο πεδία password πρέπει να είναι ίδια")]
                            )
    submit = SubmitField('Εγγραφή')

class LoginForm(FlaskForm):

    email = StringField(label='email', 
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")]
                        )
    password = PasswordField(label='password', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό")]
                            )
    submit = SubmitField('Είσοδος')