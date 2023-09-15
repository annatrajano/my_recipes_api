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

# Create a Recipe
@app.route('/recipe',  methods=['POST'])
def add_recipe():
    name = request.json['name']
    typ = request.json['typ']
    ingredients = request.json['ingredients']
    description = request.json['description']

    new_recipe = Recipe(name, typ, ingredients, description)
    db.session.add(new_recipe)
    db.session.commit()
    
    return recipe_schema.jsonify(new_recipe)

# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes_obj = Recipe.query.all()
    recipes_json = [recipe.to_json() for recipe in recipes_obj]
    return Response(json.dumps(recipes_json))

# Run Server
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
