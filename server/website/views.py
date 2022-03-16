from flask import Blueprint, render_template, request, Response, send_file
from werkzeug.utils import secure_filename
from website.models import Image
from website import db
from io import BytesIO

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")


@views.route('/list/<int:id>')
def list(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return 'Image not found', 404

    return Response(img.data, mimetype=img.mimetype)


@views.route("/upload", methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'Image not found', 404

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Upload failed', 400

    img = Image(data=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return 'Image has successfully been uploaded', 200


@views.route("/download/<int:id>")
def download(id):
    img = Image.query.filter_by(id=id).first()
    name = img.name
    if not img:
        return 'Image not found', 404

    return send_file(BytesIO(img.data), as_attachment=True, attachment_filename=name)
