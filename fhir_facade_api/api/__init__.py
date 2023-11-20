from .views import Root, ClaimsView, CreatedView, IdView, IdentifierView, SearchView, ServicedDateView
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify
from flask_restful import Api
import json


def create_app():
    app = Flask(__name__)
    app.app_context().push()
    api = Api(app)
    
    # Configure Swagger UI
    SWAGGER_URL = '/base-claims'
    API_URL = '/static/base-claims.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Base Claims API'
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/static/base-claims.json')
    def swaggger():
        with open('C:\\Users\\f9656\\Desktop\\fhir_facade\\api\\static\\base-claims.json', 'r') as file:
            return jsonify(json.load(file))

    api.add_resource(Root, '/')
    api.add_resource(ClaimsView, '/claims')
    api.add_resource(SearchView, '/claims/search')
    api.add_resource(IdView, '/claims/<string:unique_id>')
    api.add_resource(IdentifierView, '/claims/identifier/<string:identifier>')
    api.add_resource(ServicedDateView, '/claims/service-date/<string:service_date>')
    api.add_resource(CreatedView, '/claims/created-date/<string:created_date>')

    return app