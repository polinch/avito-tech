import json
from jsonschema import validate, ValidationError
from contextlib import closing

import flask
import psycopg2

AD_PER_PAGE = 10
POSTGRES = {
    'dbname': 'avito_test',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost'
}

app = flask.Flask(__name__)

all_columns = (
    'name', 'photo1', 'photo2', 'photo3', 'price', 'description'
)
columns = (
    'name', 'photo1', 'price'
)

"""
    JSON SCHEMA
"""

schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string", "maxLength": 200},
        "photo1": {"type": "string"},
        "photo2": {"type": "string"},
        "photo3": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string", "maxLength": 1000}
    },
    "required": ["name", "photo1", "photo2", "photo3", "price", "description"]
}


def connect_to_db():

    conn = psycopg2.connect(dbname=POSTGRES['dbname'], user=POSTGRES['user'], password=POSTGRES['password'],
                            host=POSTGRES['host'])

    return conn


def to_json(data):

    return json.dumps(data, indent=2) + "\n"


def response(code, data):

    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


"""
    ROUTES
"""


# sort_* = 0 - сортировка по возрастанию, 1 - по убыванию


@app.route('/ads', methods=['GET'])
def get_ads():

    try:
        page = int(flask.request.args.get("page"))
    except ValueError:
        return response(400, {})
    except TypeError:
        return response(400, {})
    sort_date = flask.request.args.get('sort_date')
    sort_price = flask.request.args.get('sort_price')

    with closing(connect_to_db()) as conn:
        with conn.cursor() as cursor:
            offset = AD_PER_PAGE * (page - 1)
            if sort_price == '1' and sort_date == '1':
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY price DESC, created_date DESC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_price == '1' and sort_date == '0':
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY price DESC, created_date ASC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_price == '0' and sort_date == '1':
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY price ASC, created_date DESC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_price == '1' and sort_date is None:
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY price DESC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_price == '0' and sort_date is None:
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY price ASC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_date == '1' and sort_price is None:
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY created_date DESC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_date == '0' and sort_price is None:
                cursor.execute("SELECT name, photo1, price FROM ad ORDER BY created_date ASC LIMIT 10 "
                               "OFFSET %s", (offset,))
            elif sort_date is None and sort_price is None:
                cursor.execute("SELECT name, photo1, price FROM ad LIMIT 10 OFFSET %s", (offset,))
            else:
                return response(400, {})

            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

    if len(results) == 0:
        return response(404, {})

    return response(200, {"Ads": results})


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):

    parameter = flask.request.args.get('parameter')
    with closing(connect_to_db()) as conn:
        with conn.cursor() as cursor:
            if parameter is None:
                cursor.execute("SELECT name, photo1, price FROM ad WHERE id=%s", (ad_id,))
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
            elif parameter == "fields":
                cursor.execute("SELECT name, photo1, photo2, photo3, price, description FROM ad WHERE id=%s", (ad_id,))
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(all_columns, row)))
            else:
                return response(400, {})

    if len(results) == 0:
        return response(404, {})

    return response(200, {"Ad": results[0]})


@app.route('/ads', methods=['POST'])
def create_new_ad():

    ad_json = flask.request.get_json()
    if ad_json is None:
        return response(400, {})
    else:
        try:
            validate(instance=ad_json, schema=schema)
        except ValidationError:
            return response(400, {})
        else:
            with closing(connect_to_db()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO ad (name, photo1, photo2, photo3, price, description) "
                                   "values (%s, %s, %s, %s, %s, %s) returning id;",
                                   (ad_json['name'], ad_json['photo1'], ad_json['photo2'], ad_json['photo3'],
                                    ad_json['price'], ad_json['description']))
                    conn.commit()
                    result = []
                    for row in cursor.fetchall():
                        result.append({"id": row[0]})

            return response(200, result[0])


if __name__ == '__main__':
    app.debug = True
    app.run()
