from flask import Blueprint, current_app, render_template
from flask_security.decorators import login_required
from radman.cache import cache
from radman.data.models import Study, Series

archive = Blueprint('archive', __name__, template_folder='templates')

@archive.route('/')
@login_required
def display_archive():
    studies = [study for study in Study.query.all()]
    current_app.logger.info('Displaying all studies.')
    return render_template("archive.htm", studies=studies)