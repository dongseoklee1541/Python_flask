from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from flask import request
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	about_me = TextAreaField(_l('About me'),
                                validators=[Length(min=0, max=140)])
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError(_('Please user a different username.'))

class PostForm(FlaskForm):
	post = TextAreaField(_l('Say something'),validators=[DataRequired()])
	submit = SubmitField(_l('Submit'))

class SearchForm(FlaskForm):
	q = StringField(_l('Search'), validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		if 'formdata' not in kwargs: # formdata : Flask-WTF가 form submission을 얻는 위치를 정한다
			kwargs['formdata'] = request.args
			"""
			기본값은 request.form 이지만 GET request를 사용할 경우 request.args를 사용해야 한다.
			"""
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False
			"""
			For clickable search links to work, CSRF needs to be disabled.
			"""
		super(SearchForm, self).__init__(*args, **kwargs)
