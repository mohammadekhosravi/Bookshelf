import os

from flask import Flask, render_template, url_for, flash, current_app, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def add_book_pic(pic_upload, name):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(name) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/book_pics', storage_filename)

    output_size = (500, 500)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, index=True)
    image = db.Column(db.String(128), nullable=False, default='default.png')
    author = db.Column(db.String(128), nullable=False, index=True)
    translator = db.Column(db.String(128), nullable=True)
    # Translated virsion publication date
    translation_date = db.Column(db.String(8), nullable=True)

    def __repr__(self):
        return f"Name: {self.name}, Author: {self.author}"

class AddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    translator = StringField('Translator')
    translation_date = StringField('Translation Date')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/add', methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        b = Book(name=form.name.data,
                 author=form.author.data)
        if form.translator.data:
            b.translator = form.translator.data

        if form.translation_date.data:
            b.translation_date = form.translation_date.data

        if form.image.data:
            pic = add_book_pic(form.image.data, form.name.data)
            b.image = pic
        db.session.add(b)
        db.session.commit()
        flash('New Book Added')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)
