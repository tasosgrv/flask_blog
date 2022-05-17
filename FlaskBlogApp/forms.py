from wsgiref.validate import validator
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from FlaskBlogApp.models import User



def maxImageSize(max_size=2):
    max_bytes = max_size*1024*1024
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"Το μεγεθος της εικόνας δεν μπορει να υπερβαινει τα {max_size} MB")

    return _check_file_size


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

    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first(): 
            raise ValidationError('Το username που δώσατε υπάρχει ήδη')

    def validate_email(self, email):
       if User.query.filter_by(email=email.data).first(): 
            raise ValidationError('Το email που δώσατε υπάρχει ήδη')


class LoginForm(FlaskForm):

    email = StringField(label='email', 
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")]
                        )
    password = PasswordField(label='password', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό")]
                            )
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField('Είσοδος')



class NewArticleForm(FlaskForm):

    article_title = StringField(label='Τίτλος', 
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                    Length(min=3, max=50, message="O τίτλος πρέπει να είναι απο 3-50 χαρακτηρες")]
                        )
    article_body = TextAreaField(label='Αρθρο', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                        Length(min=5, message="Το άρθρπ πρέπει να είναι τουλάχιστον 5 χαρακτηρες")]
                            )
    article_image = FileField(label="Εικόνα άρθρου",
                              validators=[Optional(strip_whitespace=True),
                                       FileAllowed(['jpg', 'jpeg', 'png'], 'Επιτρέοπνται μόνο αρχεία με κατάληξη .jpg .jpeg .png'),
                                       maxImageSize(max_size=2)
                                      ]
                            )
    submit = SubmitField('Ανάρτηση')


class AccountUpdateForm(FlaskForm):
    username = StringField(label='Username', 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"), 
                                        Length(min=3, max=15, message="To username πρέπει να είναι απο 3-15 χαρακτηρες")]
                            )
    email = StringField(label='email', 
                        validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να ειναι κενό"),
                                    Email(message="Παρακαλώ εισάγετε ένα σωστό email")]
                        )
    profile_image = FileField(label="Εικόνα προφίλ",
                              validators=[Optional(strip_whitespace=True),
                                       FileAllowed(['jpg', 'jpeg', 'png'], 'Επιτρέοπνται μόνο αρχεία με κατάληξη .jpg .jpeg .png'),
                                       maxImageSize(max_size=2)
                                      ]
                            )
    submit = SubmitField('Επιβεβείωση αλλαγών')

    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first(): 
                raise ValidationError('Το username που δώσατε υπάρχει ήδη')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first(): 
                    raise ValidationError('Το email που δώσατε υπάρχει ήδη')