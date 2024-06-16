from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_file = FileField('Cover Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')