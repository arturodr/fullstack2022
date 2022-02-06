# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.



## Endpoints documentation
```
Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/{question_id}'
POST '/questions/search'
GET '/categories/{category_id}/questions'
POST '/quizzes'
```

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'
- Fetches a dictionary of questions, including pagination (every 10 questions).
- Request Arguments: None
- Returns: a list of questions, number of total questions, current category, categories.  in which the keys are the ids and the value is the corresponding string of the category 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "multiple", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 27
}
```
### POST '/questions'
- POST a new question which will require the question and answer text, category, and difficulty score
- Request Arguments: question, answer, category, difficulty
- Returns: The status of the operation and the id of the created question
 
```
{
    "success": True,
    "created": 20,
}
```

### DELETE '/questions/{question_id}'
- DELETE question using a question ID
- Request Arguments: question_id
- Returns: The status of the operation and the id of the deleted question
 
```
{
    "success": True,
    "deleted": 20,
}
```

### POST '/questions/search'
- get questions based on a search term. 
- Request Arguments: searchTerm
- Returns: a list of questions, number of total questions, current category, categories.  in which the keys are the ids and the value is the corresponding string of the category 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "multiple", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### GET '/categories/{category_id}/questions'
- endpoint to get questions to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category.
- Request Arguments: previous_questions, quiz_category
- Returns: a random question
```
{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }
}
```

POST '/quizzes'

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
