from flask import Blueprint, current_app, render_template
from flask_security.decorators import roles_required
from radman.cache import cache
from radman.data.models import Study, Series

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/studies/')
@roles_required('admin','user')
@cache.cached(60)
def display_studies():
    studies = [study for study in Study.query.all()]
    current_app.logger.info('Displaying all studies.')

    return render_template("studies.htm", studies=studies)