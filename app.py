import os

from flask import Flask, render_template, url_for, flash, current_app, redirect, request
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
    hsize = 650

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(name) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/book_pics', storage_filename)

    pic = Image.open(pic_upload)
    
    hpercent = (hsize/float(pic.size[1]))
    wsize = int((float(pic.size[0]) * float(hpercent)))
    pic = pic.resize((wsize, hsize), Image.ANTIALIAS)

    pic.save(filepath)

    return storage_filename

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, index=True)
    image = db.Column(db.String(128), nullable=False, default='default.jpg')
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
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add')

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page, 4, False)

    next_url = url_for('index', page=books.next_num) \
        if books.has_next else None
    prev_url = url_for('index', page=books.prev_num) \
        if books.has_prev else None

    return render_template('index.html', books=books.items, next_url=next_url, prev_url=prev_url)

@app.route('/show_book/<int:id>')
def show_book(id):
    book = Book.query.filter_by(id=id).first()

    return render_template("show_book.html", book=book)


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
