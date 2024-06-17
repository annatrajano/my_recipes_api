from flask import Flask, request, redirect, Response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import json

from models.recipe import db, Recipe
from schemas.recipe import ma, recipe_schema, recipes_schema

# Init app
app = Flask(__name__)
CORS(app)

# Swagger UI config
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Init db and ma
db.init_app(app)
ma.init_app(app)


@app.get('/')
def home():
    """Redirect to /openapi.
    """
    return redirect('/api/docs')

# Create Response
def create_response(status, content_name, content, message=False):
    body = {}
    body[content_name] = content

    if (message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype="appication/json")


# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes_obj = Recipe.query.all()
    recipes_json = [recipe.to_json() for recipe in recipes_obj]
    return create_response(200, "recipes", recipes_json, "ok")

# Get Recipe By Id
@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    recipe_obj = Recipe.query.filter_by(id=id).first()
    if not recipe_obj:
        return create_response(404, "recipe", {}, "Recipe not found")
    recipe_json = recipe_obj.to_json()
    return create_response(200, "recipe", recipe_json, "ok")

# Create a Recipe
@app.route('/recipe',  methods=['POST'])
def add_recipe():
    body = request.get_json()

    try:
        new_recipe = Recipe(name=body["name"], typ=body["typ"],
                            ingredients=body["ingredients"], description=body["description"])
        db.session.add(new_recipe)
        db.session.commit()
        return create_response(201, "recipe", new_recipe.to_json(), "Recipe created successfully")
    except Exception as e:
        print('Error', e)
        return create_response(400, "recipe", {}, "Error")
    
# Update Recipe By Id
@app.route('/recipe/<id>', methods=['PUT'])
def update_recipe(id):
    recipe_obj = Recipe.query.filter_by(id=id).first()
    if not recipe_obj:
        return create_response(404, "recipe", {}, "Recipe not found")
    
    body = request.get_json()
    try:
        if all(key in body for key in ('name', 'typ', 'ingredients', 'description')):
            recipe_obj.name = body['name']
            recipe_obj.typ = body['typ']
            recipe_obj.ingredients = body['ingredients']
            recipe_obj.description = body['description']
            
            db.session.add(recipe_obj)
            db.session.commit()
            return create_response(200, "recipe", recipe_obj.to_json(), "Recipe updated successfully")
        else:
            return create_response(400, "recipe", {}, "Missing fields in request body")
    except Exception as e:
        print('Error', e)
        return create_response(400, "recipe", {}, "Error")

# Delete a Recipe
@app.route('/recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    recipe_obj = Recipe.query.filter_by(id=id).first()
    if not recipe_obj:
        return create_response(404, "recipe", {}, "Recipe not found")
    
    try:
        db.session.delete(recipe_obj)
        db.session.commit()
        return create_response(200, "recipe", recipe_obj.to_json(), "Recipe deleted successfully")
    except Exception as e:
        print('Error', e)
        return create_response(400, "recipe", {}, "Error")


# Run Server
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
