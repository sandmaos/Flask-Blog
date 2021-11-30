from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import User


class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    author = StringField('Your mood?', validators=[DataRequired(), Length(1, 30), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Username must only have '
                                                                                         'letters, numbers, '
                                                                                         'dots or underscores')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 30), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 30), Email()])
    name = StringField('Username', validators=[DataRequired(), Length(1, 30), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                     'Username must only have '
                                                                                     'letters, numbers, '
                                                                                     'dots or underscores')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username is already in use.')


class EditForm(FlaskForm):
    about = TextAreaField('About', validators=[DataRequired()])
    name = StringField('Username', validators=[DataRequired(), Length(1, 30), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                     'Username must only have '
                                                                                     'letters, numbers, '
                                                                                     'dots or underscores')])
    location = StringField('Location', validators=[DataRequired()])
    birth = DateField('Birthday', validators=[DataRequired()])
    submit = SubmitField('Confirm')


class EditPasswordForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Confirm')


class EditPostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Confirm')


class CommentForm(FlaskForm):
    comment = StringField("What's your opinion?", validators=[DataRequired()])
    submit = SubmitField('Confirm')
