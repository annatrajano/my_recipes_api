from flask import Flask, request, jsonify, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_openapi3 import OpenAPI, Info, Tag
import json
import os

# Init app
# tags
home_tag = Tag(name="Documentation", description="Swagger, Redoc ou RapiDoc")
recipe_tag = Tag(
    name="Recipe", description="Add, view and delete recipes from the base")
info = Info(title="My Recipes API", version="1.0.0")
app = OpenAPI(__name__, info=info)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Recipe Class/Model


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    typ = db.Column(db.String(140))
    ingredients = db.Column(db.String(500))
    description = db.Column(db.String(500))

    def to_json(self):
        return {"id":self.id, "name":self.name, "typ":self.typ, "ingredients":self.ingredients, "description":self.description}


# Recipe Schema


class RecipeSchema(ma.Schema):
    class Meta:
        fields: ('id', 'name', 'typ', 'ingredients', 'description')


# Init Schema
recipe_schema = RecipeSchema
recipes_schema = RecipeSchema(many=True)


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi.
    """
    return redirect('/openapi')

# Create Response
def create_response(status, content_name, content, message=False):
    body={}
    body[content_name] = content
    
    if(message):
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
    recipe_json = recipe_obj.to_json()
    return create_response(200, "recipe", recipe_json, "ok")

# Create a Recipe
@app.route('/recipe',  methods=['POST'])
def add_recipe():
    body = request.get_json()
    
    try:
        new_recipe = Recipe(name=body["name"], typ=body["typ"], ingredients=body["ingredients"], description=body["description"])
        db.session.add(new_recipe)
        db.session.commit()
        return create_response(201, "recipe", new_recipe.to_json(), "Recipe created successfully")
    except Exception as e:
        return create_response(400, "recipe", {}, "Error")
    

# Run Server
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
