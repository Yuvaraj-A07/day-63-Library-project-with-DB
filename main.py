from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# LIBRARY MANAGEMENT USING FORMS AND SQL DB

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///library.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()


# all_books = []


@app.route('/')
def home():
    # getting the book details

    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()

    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    # ADDING THE BOOK DETAILS THAT THE USER ENTERS
    if request.method == "POST":
        data = request.form
        book_name = data["b_name"]
        book_author = data["b_author"]
        rating = data["b_rating"]

        # book_info = {
        #     "title": book_name,
        #     "author": book_author,
        #     "rating": rating
        # }
        # all_books.append(book_info)
        # print(all_books)

        new_book = Book(title=book_name, author=book_author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    # BEFORE ADDING THE BOOK DETAILS
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    # EDITING THE BOOK RATING
    if request.method == "POST":
        book_id = request.args.get('id')
        change_rating = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        change_rating.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    # IT'S BEFORE EDITING THE BOOK DETAILS GETTING THE INPUT FROM USER LIKE WHICH BOOK YOU NEED TO EDIT
    book_id = request.args.get('id')
    book_selected = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    return render_template("edit.html", selected=book_selected)


@app.route("/delete")
def delete():
    # DELETING THE BOOK THAT WHICH THE USER CLICKED
    book_id = request.args.get('id')
    book_selected = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_selected)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
