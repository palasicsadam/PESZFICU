from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from website.models import Images, Person, Report
from website import db
from io import BytesIO
from base64 import b64encode


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('index.html')


@views.route('/list')
def list():
    ppl = Person.query.order_by(Person.person_id).all()

    for person in ppl:
        if not person.desc:
            person.desc='No description'

    return render_template('list.html', ppl=ppl)


@views.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    desc = request.form.get('description')
    if not name:
        flash('No name entered', category='error')
        return render_template('index.html')

    person = Person(name=name, desc=desc)
    db.session.add(person)
    db.session.commit()

    flash('Person has been successfully added')

    return render_template("index.html")


@views.route('/view/<int:pid>', methods=['GET'])
def view(pid):
    person = Person.query.get({'person_id': pid})

    if not person.desc:
        person.desc = 'No description'

    if request.form.get('edit_profile') == 'edit':
        return render_template('edit.html', person=person)

    images = {}
    data = Images.query.filter(Images.person_id == pid).all()
    num_of_rows = (len(data) // 3) + 1

    if len(data) != 0:
        for item in data:
            img = b64encode(item.image).decode('utf-8')
            img_id = item.id
            images[img_id] = img
        return render_template('view.html', person=person, images=images, num_of_rows=num_of_rows)
    else:
        return render_template('view.html', person=person)


@views.route('/remove/<int:pid>')
def remove(pid):
    Person.query.filter_by(person_id=pid).delete()
    Images.query.filter_by(person_id=pid).delete()
    db.session.commit()
    return redirect(url_for('views.list'))


@views.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit(pid):
    person = Person.query.get({'person_id': pid})
    name = request.form.get('name')
    desc = request.form.get('description')
    if not name and not desc:
        flash('Enter a name or description')
        return render_template('edit.html', person=person)
    if name:
        db.session.query(Person).filter(Person.person_id == pid).update({'name': name, 'desc': desc})
        db.session.commit()
        flash('Person\'s profile has successfully been updated')
    return redirect(url_for('views.view', pid=pid))


@views.route('/view/<int:pid>', methods=['POST'])
def upload(pid):
    input_file = request.files.get('input')
    if input_file:
        img = Images(image=input_file.read(), person_id=pid)
        db.session.add(img)
        db.session.commit()
        flash('Image has successfully been uploaded')
        return view(pid)
    if not input_file:
        flash('No image has been selected', category='error')  # appears when you click the edit button
        return view(pid)


@views.route('/delete/<int:id>')
def delete(id):
    img = Images.query.filter_by(id=id).first()
    Images.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('views.view', pid=img.person_id))


@views.route('/download/<int:id>', methods=['GET'])
def download(id):
    img = Images.query.filter_by(id=id).first()
    file_name = str(img.person_id) + '_' + str(img.id) + '.jpg'
    return send_file(BytesIO(img.image), as_attachment=True, download_name=file_name)