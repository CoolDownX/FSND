import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

# Public Route for /drinks - no auth
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        get_drinks = db.session.query(Drink) \
            .all()
        formated_result = [drink.short() for drink in get_drinks]
    except:
        abort(500)

    return jsonify({
        'success': True,
        'drinks': formated_result
    })

# Route for Drinks detail 
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try: 
        get_data = db.session.query(Drink) \
            .all()
        get_drinks_details = [
                                drink.long() 
                                for drink in get_data
                            ]
    except:
        abort(500)

    return jsonify({
        'success': True,
        'drinks': get_drinks_details
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_new_drink(jwt):

    # Get JSON data from requqest
    title = request.json.get('title')

    # Check if the variable contains a Value
    if title == "":
        abort(400)

    # Format recipe the right way
    try: 
        recipe = [{
                    'name': r['name'], 
                    'color': r['color'], 
                    'parts': r['parts']
                    } 
                    for r in request.json['recipe']
                ]

    # Transform into a String to save it in the db
        recipe = json.dumps(recipe)
    
    except: 
        abort(400)

    try:
        new_drink = Drink( \
                                title = title, \
                                recipe = recipe, \
                            )
        new_drink.insert()
        
        new_drink = Drink.long(new_drink)

    except:
        abort(422)
    
    return jsonify({
        'success': True,
        'drinks': new_drink
    })

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_existing_drink(jwt, drink_id):

    existing_drink = db.session.query(Drink) \
        .filter(Drink.id == drink_id) \
        .one_or_none()

    if existing_drink is None:
        abort(404)

    # Get JSON data from requqest
    if 'title' in request.json:
        title = request.json.get('title')
        existing_drink.title = title

    # Format recipe the right way
    if 'recipe' in request.json:
        try: 
            recipe = [{
                        'name': r['name'], 
                        'color': r['color'], 
                        'parts': r['parts']
                        } 
                        for r in request.json['recipe']
                    ]

            # Transform into a String to save it in the db
            recipe = json.dumps(recipe)
            existing_drink.recipe = recipe

        except: 
            abort(400)
    
    db.session.commit()

    existing_drink = Drink.long(existing_drink)

    return jsonify({
        'success': True,
        'drinks': existing_drink
    })

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    
    delete_drink = db.session.query(Drink) \
        .filter(Drink.id == drink_id) \
        .one_or_none()
    
    if delete_drink is None:
        abort(404)

    elif delete_drink is not None:
        try:
            delete_drink.delete()
        except:
            abort(500)

    return jsonify({
        'success':  True,
        'delete':   delete_drink.id
    })

## Error Handling

@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400

@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "Unauthorized"
                    }), 401

@app.errorhandler(403)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "Forbidden"
                    }), 403

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not found"
                    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "Internal Server Error"
                    }), 500

@app.errorhandler(AuthError)
def Authentification_Error(e):
    return jsonify({
                    "success": False, 
                    "error": e.error['code'],
                    "message": e.error['description']
                    }), e.status_code

