import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@ uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
# db_drop_and_create_all()

# ROUTES


@app.route("/drinks", methods=["GET"])
def get_drinks():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    drinks_short = [drink.short() for drink in drinks]

    return jsonify(
        {
            "success": True,
            "drinks": drinks_short,
        }
    )


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail():
    """
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    drinks_long = [drink.long() for drink in drinks]

    return jsonify(
        {
            "success": True,
            "drinks": drinks_long,
        }
    )


@app.route("/drinks", methods=["POST"])
@requires_auth('post:drinks')
def post_drink():
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    """
    try:
        data = request.get_json()
        drink = Drink(title=data['title'],
                      recipe=json.dumps(data['recipe']))
        drink.insert()
    except Exception as e:
        print(e)
        drink.rollback()
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def patch_drink(drink_id):
    """
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    data = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)

    drink.title = data.get("title", drink.title)
    drink.recipe = data.get("recipe", drink.recipe)

    # if we are updating the recipe, we get an obj that needs conversion
    if isinstance(drink.recipe, list):
        drink.recipe = json.dumps(drink.recipe)

    drink.update()

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    """
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)

    drink.delete()

    return jsonify({
        "success": True,
        "delete": drink_id
    }), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
    implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(404)
def not_found(error):
    """
        implement error handler for 404
        error handler should conform to general task above
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def permission_error(error):
    """
        implement error handler for AuthError
        error handler should conform to general task above
    """
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Authentication error"
    }), 401


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code


if __name__ == "__main__":
    app.debug = True
    app.run()
