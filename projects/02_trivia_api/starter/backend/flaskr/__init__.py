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
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
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
                "categories": {category.id: category.type for category in categories},
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
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route("/questions", methods=["GET"])
    def get_questions():
        # Implement pagination
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "questions": formatted_questions[start:end],
                "total_questions": len(questions),
                "categories": {category.id: category.type for category in categories},
                "currentCategory": "multiple"
            }
        )

    '''
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        except:
            abort(422)

    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            flash('question was successfully created!')

            return jsonify({
                'success': True,
                'created': question.id,
            })

        except Exception as e:
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
        search = body.get("searchTerm", "").lower()
        questions = Question.query.filter(func.lower(Question.question).contains(search)).all()

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
        # Implement pagination
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.filter(Question.category == category_id)
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "questions": formatted_questions[start:end],
                "total_questions": len(formatted_questions),
                "categories": {category.id: category.type for category in categories},
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

        question = Question.query\
            .filter(Question.category == quiz_category.get('id'))\
            .filter(Question.id.notin_(previous_questions))\
            .order_by(func.random()).limit(1)

        if question:
            question = dict(question[0].format())
        return jsonify({'question': question})

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
