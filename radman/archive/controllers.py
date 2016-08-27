from flask import Blueprint, current_app, render_template,request
from flask_security.decorators import login_required
from radman.cache import cache
from radman.data.models import Study, Series
import datetime

archive = Blueprint('archive', __name__, template_folder='templates')

@archive.route('/')
@login_required
def display_archive():
    date_range = request.args.get('date_range')
    if request.args.get('date_range'):
        date_from = request.args.get('date_range').split(" to ")[0]
        date_to = request.args.get('date_range').split(" to ")[1]
    else:
        date_from = (datetime.datetime.now() + datetime.timedelta(-30)).strftime("%Y-%m-%d")
        date_to = datetime.datetime.now().strftime("%Y-%m-%d")

    return render_template("archive.htm",accession_number = request.args.get('accession_number'),
                           patient_name = request.args.get('patient_name'),
                           patient_id = request.args.get('patient_id'),
                           station_name = request.args.get('station_name'),
                           description = request.args.get('description'),
                           date_from = date_from,
                           date_to = date_to)
