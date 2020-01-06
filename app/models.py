from datetime import datetime
import json
from app import db


class Ad:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    photo1 = db.Column(db.String)
    photo2 = db.Column(db.String)
    photo3 = db.Column(db.String)
    description = db.Column(db.String(1000))

    @classmethod
    def get(cls):
        return json.dumps({
            'id': cls.id,
            'name': cls.name,
            'price': cls.price,
            'photo': cls.photo1
        })

    @classmethod
    def get_all_fields(cls):
        return json.dumps({
            'id': cls.id,
            'name': cls.name,
            'price': cls.price,
            'description': cls.description,
            'photos': [
                {'photo1': cls.photo1},
                {'photo2': cls.photo2},
                {'photo3': cls.photo3}
            ]
        })
