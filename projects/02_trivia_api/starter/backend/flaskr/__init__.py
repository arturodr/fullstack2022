import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "udacity"

    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": '*'}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
        )
        return response

    '''
    Create an endpoint to handle GET requests for all available categories.
    '''

    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type
                               for category in categories},
                "total_categories": len(categories),
            }
        )

    '''
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    def get_formatted_questions(page=1, category_id=0):
        # generic function to get page of questions
        current_index = page - 1
        if category_id == 0:
            questions = Question.query.order_by(Question.id) \
                .limit(QUESTIONS_PER_PAGE) \
                .offset(current_index * QUESTIONS_PER_PAGE).all()
            total_questions = Question.total_questions()
        else:
            questions = Question.query.order_by(Question.id) \
                .filter(Question.category == category_id) \
                .limit(QUESTIONS_PER_PAGE) \
                .offset(current_index * QUESTIONS_PER_PAGE).all()
            total_questions = Question.query \
                .filter(Question.category == category_id).count()

        formatted_questions = [question.format() for question in questions]

        return formatted_questions, total_questions

    @app.route("/questions", methods=["GET"])
    def get_questions():
        page = request.args.get("page", 1, type=int)
        questions, total_questions = get_formatted_questions(page)

        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "questions": questions,
                "total_questions": total_questions,
                "categories": {category.id: category.type
                               for category in categories},
                "currentCategory": "multiple"
            }
        )

    '''
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        except Exception as e:
            print(e)
            question.rollback()
            abort(422)

    '''
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the
    end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if (new_question is None or new_answer is None or
                new_category is None or new_difficulty is None):
            abort(422)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            flash('question was successfully created!')

            return jsonify({
                'success': True,
                'created': question.id,
            })

        except Exception as e:
            print(e)
            question.rollback()
            abort(422)

    '''
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route("/questions/search", methods=["POST"])
    def search_questions():

        body = request.get_json()
        searchTerm = body.get("searchTerm", "").lower()
        if searchTerm == "":
            abort(422)
        questions = Question.query.filter(
            func.lower(Question.question).contains(searchTerm)).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(questions),
            "currentCategory": "multiple"
        })

    '''
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_questions_in_category(category_id):
        if not category_id:
            abort(422)

        page = request.args.get("page", 1, type=int)
        questions, total_questions = get_formatted_questions(page, category_id)

        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "questions": questions,
                "total_questions": total_questions,
                "categories": {category.id: category.type
                               for category in categories},
                "currentCategory": category_id
            }
        )

    '''
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play():
        data = request.json
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        if not quiz_category or quiz_category.get('id') is None:
            abort(422)

        if quiz_category.get('id') == 0:
            question = Question.query \
                .filter(Question.id.notin_(previous_questions)) \
                .order_by(func.random()).limit(1)
        else:
            question = Question.query \
                .filter(Question.category == quiz_category.get('id')) \
                .filter(Question.id.notin_(previous_questions)) \
                .order_by(func.random()).limit(1)

        if question[0] is not None:
            question = dict(question[0].format())
        else:
            abort(404)
        return jsonify({"success": True, 'question': question})

    '''
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def sever_error(error):
        return jsonify({
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
