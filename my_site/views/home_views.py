import flask
from infrastructure.view_modifiers import response
import services.package_service as package_service

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    packages = package_service.get_latest_packages()
    return {'packages': packages}


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    return {}
