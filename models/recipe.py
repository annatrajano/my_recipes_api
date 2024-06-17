from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    typ = db.Column(db.String(140))
    ingredients = db.Column(db.String(500))
    description = db.Column(db.String(500))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "typ": self.typ,
            "ingredients": self.ingredients,
            "description": self.description
        }