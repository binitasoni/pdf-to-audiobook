import io
import os
from flask import Flask, render_template, redirect, url_for, request
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import pyttsx3
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
# initialisation
def extract_text(pdf_path,audio_name):
    for page in extract_text_by_page(pdf_path):
        print(page)
        text_to_speech(page,audio_name)

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()
def text_to_speech(mytext,filename):
    engine = pyttsx3.init()
    engine.save_to_file(mytext,f'{filename}.mp3')
    engine.runAndWait()

try:

    from flask import Flask

    from flask import redirect, url_for, request, render_template, send_file
    from io import BytesIO

    from flask_wtf.file import FileField
    from wtforms import SubmitField
    from flask_wtf import FlaskForm
    import sqlite3
    print("All Modules Loaded .... ")
except:
    print (" Some Module are missing ...... ")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
bootstrap = Bootstrap(app)
class UploadForm(FlaskForm):
    file = FileField()
    audio_name=StringField("Add Name of your audio file")
    submit = SubmitField("submit")
    download = SubmitField("download")

@app.route('/', methods=["GET", "POST"])
def index():

    form = UploadForm()
    if request.method == "POST":

        if form.validate_on_submit():
            file_name = form.file.data
            audio_name=form.audio_name.data
            file_name.save(os.path.join("/Users/anupamsarfare/PycharmProjects/pythonProject/pdf-to-text", file_name.filename))
            extract_text(f"/Users/anupamsarfare/PycharmProjects/pythonProject/pdf-to-text/{file_name.filename}",audio_name)
            return render_template("index.html", form=form)

    return render_template("index.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)