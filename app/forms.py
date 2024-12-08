from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_wtf.file import FileRequired


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4, max=100)]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4, max=100)]
    )
    submit = SubmitField('Login')


class AddDomainForm(FlaskForm):
    domain_name = StringField(
        "Domain Name",
        validators=[
            DataRequired(message="Domain name is required"),
            Regexp(
                r"^(?!-)(?:[A-Za-z0-9-]{1,120}(?=\.[A-Za-z0-9-]{2,})(?:\.[A-Za-z]{2,}){1,3})$",
                message="Invalid domain format",
            ),
        ],
    )
    submit = SubmitField("Add Domain")


class BulkUploadForm(FlaskForm):
    file = FileField(
        "Bulk File upload",
        validators=[FileRequired(message="A file is required for bulk upload")],
    )
    submit = SubmitField("Upload Domains")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired(message="Current password is required.")]
    )
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(message="New password is required.")]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message="Please confirm your new password."),
            EqualTo('new_password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Change Password')
