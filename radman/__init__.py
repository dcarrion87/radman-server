from flask import abort, Flask, g, render_template, request,session
from flask_babel import Babel
from flask_security import current_user
from flask_security.decorators import login_required
from radman.utils import get_instance_folder_path
from radman.archive.controllers import archive
from radman.cache import cache
from radman.config import configure_app
from radman.data.models import Study,Series,Instance, db
from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='templates')

babel = Babel(app)
configure_app(app)
# Not needed
#cache.init_app(app)
db.init_app(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@app.url_defaults
def set_language_code(endpoint, values):
    if 'lang_code' in values or not g.get('lang_code', None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code

@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)

@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)

@babel.localeselector
def get_locale():
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path, error))
    return render_template('404.htm'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.htm'), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.htm'), 500

@app.context_processor
def inject_data():
    return dict(user=current_user, \
        lang_code=g.get('lang_code', None))

@app.route('/')
@app.route('/<lang_code>/')
@login_required
def home(lang_code=None):
    return render_template('index.htm')

app.register_blueprint(archive, url_prefix='/archive')

def api_auth_func(**kw):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Authentication required', code=401)

api_manager = APIManager(app,
                         flask_sqlalchemy_db=db,
                         preprocessors=dict(GET_SINGLE=[api_auth_func],
                                            GET_MANY=[api_auth_func])
                         )
api_manager.create_api(Study,
                       methods=['GET'],
                       url_prefix='/api/v1')
api_manager.create_api(Series,
                       methods=['GET'],
                       url_prefix='/api/v1')
api_manager.create_api(Instance,
                       methods=['GET'],
                       url_prefix='/api/v1')
