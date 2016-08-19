from flask import Blueprint, render_template, flash
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required
from radman.admin.forms.author_forms import CreateAuthorForm
from radman.cache import cache
from radman.data.models import Study, db
from sqlalchemy import exc


admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@roles_required('admin')
def index():
    return render_template('admin_index.htm')

@admin.route('/author/create', methods=['GET', 'POST'])
@roles_required('admin')
def create_author():
    form = CreateAuthorForm(request.form)
    if request.method == 'POST' and form.validate():
        names = form.names.data
        current_app.logger.info('Adding a new author %s.', (names))
        author = Study(names)

        try:
            db.session.add(author)
            db.session.commit()
            cache.clear()
            flash('Study successfully created.')
        except exc.SQLAlchemyError as e:
            flash('Study was not created.')
            current_app.logger.error(e)

            return redirect(url_for('admin.create_author'))

        return redirect(url_for('main.display_authors'))

    return render_template('create_author.htm', form=form)
