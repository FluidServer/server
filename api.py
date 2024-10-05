# 💧 FluidServer
# by clue <lost@biitle.nl>

version = "1.0"

fsSettings = {
    "port": 1618,
    "legacy-port": 80,
    "swagger-ui-version": 3,
    "db": "./tests/test.db"
}

import argparse
from datetime import datetime
import sqlite3
from flask import Flask, g, request, send_from_directory, render_template
from flasgger import Swagger
from flasgger import swag_from # swag!

parser = argparse.ArgumentParser(
    prog = "FluidServer",
    description = "FluidServer FOSS POS-system server",
    epilog='built by clue <lost@biitle.nl> FluidServer (fs.biitle.nl)')

parser.add_argument("-p", "--port", help = "Server port (default: 1618)")
parser.add_argument("-d", "--database", help = "Database (default: ./tests/test.db)")
parser.add_argument("-s", "--swagger", help = "Swagger UI Version (default: 3)")

args = parser.parse_args()

if args.port:
    fsSettings['port'] = args.port
if args.database:
    fsSettings['db'] = args.database
if args.swagger:
    fsSettings['swagger-ui-version'] = args.swagger

app = Flask(__name__)
database = fsSettings["db"]

@app.route('/data/<path:filename>')
def serve_file(filename):
    """
    Serves files in data directory.
    """
    return send_from_directory('data', filename)

app.config["SWAGGER"] = {
    "title": "FluidServer",
    "uiversion": int(fsSettings["swagger-ui-version"]),
}

swag = Swagger(app,
    decorators=[],
    template={
        "swagger": "2.0",
        "info": {
            "title": "FluidServer: Open-source POS-system server",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def get_db():
    """
    Gets database for usage.
    Uses database in `database` variable.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes database connection.
    Run this before closing program.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
    Queries the database.
    `query`: The query you want to run.
    `args`: What variable `?` is replaced with.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    """
    Homepage. Shows `templates/index.html`
    """
    return render_template("index.html" , version=version, year=datetime.now().year)

@app.route('/api/control/<int:barcode>', methods=['GET'])
@swag_from("data/control.yml")
def control(barcode: int) -> str:
    """
    Deprecated. Use `product` instead.

    Checks if a product is controlled or not.
    Useful for pharmacies.
    `barcode`: Barcode of the product.

    Expected output:
    If the product is controlled or not. Example: `1` (controlled)
    """
    if request.is_json == True:
        json = request.get_json()
        if json['barcode'] is not None:
            barcode = str(json['barcode'])
    item = query_db('SELECT * FROM controlled WHERE Barcode = ?',
                    [barcode], one=True)

    if item is None:
        return 'null'
    else:
        return str(item['IsControl'])

@app.route('/api/user/<int:userid>', methods=['GET'])
@swag_from("data/user.yml")
def exists(userid: int) -> str:
    """
    Gets user name.
    `userid`: ID of the user.

    Expected output:
    User name. Example: `John Doe`
    """
    if request.is_json == True:
        json = request.get_json()
        if json['user'] is not None:
            userid = str(json['userid'])
    user = query_db('SELECT * FROM users WHERE UserID = ?', 
                    [userid], one=True)

    if user is None:
        return 'null'
    


    if user is None:
        return 'null'
    else:
        return str(user['Name'])

@app.route('/api/product/<int:barcode>', methods=['GET'])
@swag_from("data/product.yml")
def product(barcode: int) -> str:
    """
    Use this instead of `control`.
    Gets product data in
    name|price|type (UN/KG)|controlled format.
    `barcode`: Barcode of the product.

    Expected output:
    Product Data. Example: `1|Test Product|19,90|0`
    """
    if request.is_json == True:
        json = request.get_json()
        if json['barcode'] is not None:
            barcode = str(json['barcode'])
    data = query_db('SELECT * FROM products WHERE Barcode = ?',
                    [barcode], one=True)
    
    control = query_db('SELECT * FROM controlled WHERE Barcode = ?',
                       [barcode], one=True)
    
    if data is None:
        return 'null'

    if control is None:
        return 'null'

    name = str(data['Name'])
    price = str(data['PriceUn'])
    btype = str(data['BaseType'])
    bcontrol = str(control['IsControl'])

    fname = name.replace('|', '\\|')
    fprice = price.replace('|', '\\|')
    ftype = btype.replace('|', '\\|')
    fcontrol = bcontrol.replace('|', '\\|')

    finalout = str(fname) + '|' + str(fprice) + '|' + str(ftype) + "|" + fcontrol

    
    return str(finalout)

"""
@app.route('/api/list/', methods=['GET'])
def list():
    data = query_db('SELECT * FROM products;', one=True)

    if data is None:
        return 'null'

    return str(data)
"""

""" STOCK SYSTEM """

@app.route('/stock/location/<int:barcode>', methods=['GET'])
@swag_from("data/stock/location.yml")
def stockLocate(barcode: int) -> str:
    """
    Locate a product in stock.
    `barcode`: Barcode of the product.

    Expected output:
    Stock Location. Example: `A1:1` (product location)
    """
    item = query_db('SELECT * FROM place WHERE Barcode = ?',
                            [barcode], one=True)

    if item is None:
        return 'null'
    else:
        return str(item['Place'])

@app.route('/stock/quantity/<int:barcode>', methods=['GET'])
@swag_from("data/stock/quantity.yml")
def stockQuantity(barcode: int) -> str:
    """
    Get quantity of a product in stock.
    `barcode`: Barcode of the product.

    Expected output:
    Quantity of product. Example: `400`
    """
    item = query_db('SELECT * FROM stock WHERE Barcode = ?',
                          [barcode], one=True)

    if item is None:
        return 'null'
    else:
        return str(item['InStock'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=fsSettings["port"])
