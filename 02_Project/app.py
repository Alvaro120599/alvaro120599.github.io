from flask import Flask
from flask import request
from pypdf import PdfReader


app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/read')
def read():
    data = {}
    reader = PdfReader("data/faq.pdf")
    number_of_pages = len(reader.pages)
    text = ""
    for i in range(0, number_of_pages):
        page = reader.pages[i]
        text = text + "\n" + page.extract_text()
    data["pages"] = number_of_pages
    data["text"] = text
    return data


# /read/faq.pdf/3

@app.route('/read/<name>/<int:page_number>')
def read_page(name, page_number):
    data = {}
    reader = PdfReader("data/{}".format(name))
    number_of_pages = len(reader.pages)
    page = reader.pages[page_number]
    data["page"] = page_number
    data["text"] = page.extract_text()
    return data