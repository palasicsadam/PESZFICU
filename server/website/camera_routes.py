"""
The routes in this file are for the camera software to use
"""
from flask import Blueprint, request, send_file
from io import BytesIO
from .models import Report, Images, Person
from website import db
from datetime import datetime

camera = Blueprint('camera', __name__)


@camera.route('/list', methods=['GET'])
def list_images():
    """
    Lists the images in db in JSON format like below:
    {
        person_id1: [image_id1, image_id2, ....],
        person_id2: [image_id1, image_id2, ....],
    }
    If no images sends an empty json object.
    :return:
    """
    data = Images.query.all()
    json_response = {}
    for image in data:
        if image.person_id not in json_response:
            json_response[image.person_id] = []
        json_response[image.person_id].append(image.id)
    return json_response


@camera.route('report', methods=['POST'])
def submit_report():
    """
    Handles the uploading of reports.
    Reports should be sent in the form of a JSON object of the following format:
    {
        "report" : {
            "people": [id1, id2, ...], // a list of ids
            "camera_name": "example", // name of camera
            "time_stamp": 121323434 // unix timestamp, easier to convert than string time
            "b64_image": "eegkegfkejfwejhdu3iukgb==" // base64 encoded image
        }
    }
    :return:
    """
    try:
        report_details = request.get_json()['report']
        time_stamp = datetime.fromtimestamp(report_details['time_stamp'])
        camera_name = report_details['camera_name']
        b64_image = report_details['b64_image']
        for person in report_details['people']:
            report = Report(
                person_id=person,
                camera_name=camera_name,
                time_stamp=time_stamp,
                b64_image=b64_image
            )
            db.session.add(report)

        db.session.commit()
        return {'Status': 'Success'}
    except Exception as e:
        return {'Status': 'Error'}, 400


@camera.route('download/<int:id>', methods=['GET'])
def download_image(id):
    """
    Donwload the image with th specified id.
    :param id:
    :return:
    """
    img = Images.query.filter_by(id=id).first()
    file_name = str(img.person_id) + '_' + str(img.id) + '.jpg'
    return send_file(BytesIO(img.image), as_attachment=True, download_name=file_name)
