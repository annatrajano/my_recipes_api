from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'typ', 'ingredients', 'description')

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
