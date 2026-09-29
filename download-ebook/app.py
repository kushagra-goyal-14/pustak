from flask import Flask,render_template,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from downloader import download

app = Flask(__name__)
app.config['SECRET_KEY'] = "YOUR_KEY"     # Replace this value before deployment.

# Accept a book title or a supported store link.
class book_form(FlaskForm):

    book_link = StringField("Book title or link")
    author = StringField("Author (optional)")
    file_format = SelectField("Format", choices=[("pdf", "PDF"), ("epub", "EPUB")], default="pdf")
    submit = SubmitField("Find ebook")

book_link = None

# Show the search form and handle submissions.
@app.route('/',methods=['GET','POST'])
def download_ebook():

    form = book_form()

    if form.validate_on_submit():

        book_link = form.book_link.data.strip()   # Ignore leading and trailing spaces.

        author = form.author.data.strip()
        if not book_link and not author:
            form.book_link.errors.append("Enter a book title, link, or author.")
            return render_template("home.html", form=form)

        try:

            download_link = download(book_link, form.file_format.data, author)          # Resolve the title to a download link.

            return redirect(download_link)

        except Exception:

            return render_template("notfound.html")


    return render_template("home.html",form=form)

if __name__ == '__main__':

    app.run()
