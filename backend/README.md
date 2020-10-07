# Full Stack Trivia API Backend

## Getting Started

### Dependencies

Dependencies are listed in the `requirements.txt` file. 
Run `pip3 install -r requirements.txt` to install them.

### Tech Stack

* SQLAlchemy ORM
* PostgreSQL
* Python3 and Flask
* Flask-Migrate
* Flask-CORS
* HTML, CSS, and Javascript

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints
### Categories
#### `GET /categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments : None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

#### `Response`
```json
{ 
    "success": true,
    "categories": {
        "1" : "Science", 
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    }
}
```

#### `GET /questions?page=1`

- Fetches a list of dictionaries of paginated questions in which each question is an object with its own values
- Fetches a dictionary of categories in which the keys are the ids, and the values are the corresponding strings of the categories
- Fetches the total number of questions, and current category which is set to None
- Request Arguments : None
- Request Query Parameters : "page" parameter defaults to 1
- Returns: A list of objects contain key:value pairs of id, question, answer, difficulty and category

#### `Response`
```json5
{
    "success" : true,
    "questions": [
                    { 
                        "id" : 1,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                ]
    "total_questions": 1,
    "current_category" : "None",
    "categories" : {      
                        "1" : "Science", 
                        "2" : "Art",
                        "3" : "Geography",
                        "4" : "History",
                        "5" : "Entertainment",
                        "6" : "Sports"
                   }
}
```
    
#### `POST /questions`

- Creates a question sent by request"s body
- Fetches a list of dictionaries of paginated questions in which each question is an object with it"s own values
- Request Arguments : None
- Returns The created question"s id, the list of questions, and the total number of questions

#### `Response`
```json5
{
    "success" : true,
    "created" : 2,
    "questions": [
                    { 
                        "id" : 1,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                    { 
                        "id" : 2,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                ]
    "total_questions": 2,
}
```

#### `POST /questions/search`

- Searches for provided search term in the form
- Fetches a list of dictionaries of paginated questions in which each question is an object with it"s own values
- Request Arguments : None
- Returns: a list of questions that contain the provided search term

#### `Response`
```json5
{
    "success" : true,
    "questions": [
                    { 
                        "id" : 1,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                    { 
                        "id" : 2,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                ]
    "total_questions": 2,
}
```

#### `DELETE /questions/<int:question_id>`
- Deletes a question based on the provided variable which maps to the id of the question
- Fetches a list of dictionaries of paginated questions in which each question is an object with it"s own values
- Request Arguments : Question id to be deleted
- Returns: The deleted question"s id, the list of questions, and the total number of questions
       
#### `Response`       
```json5
{
    "success" : true,
    "deleted" : 1,
    "questions": [
                    { 
                        "id" : 2,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                ]
    "total_questions": 1,
}
```

#### `POST /categories/<category_type>/questions`

- Retrieve questions based on the Category Type variable
- Fetches a list of dictionaries of paginated questions in which each question is an object with it"s own values
- Request Arguments : Category Type
- Returns: a list of questions within that Category Type

#### `Response`
```json5
{
    "success" : true,
    "questions": [
                    { 
                        "id" : 1,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                    { 
                        "id" : 2,
                        "question" : "What is testing",
                        "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                        "category": "Programming",
                        "difficulty": 3
                    } 
                ]
    "total_questions": 2,
}
```

#### `POST /play`

- Fetches a question based on the category type
- Request Arguments : None
- Returns a random question within the selected category

#### `Response`
```json5
{
    "success" : true,
    "questions": { 
                    "id" : 1,
                    "question" : "What is testing",
                    "answer" : "Software testing is an investigation conducted to provide information about the quality of the software product or service under test"
                    "category": "Programming",
                    "difficulty": 3
                 } 
}
```


## Status Codes
- `200` : Request has been fulfilled
- `201` : Entity has been created
- `400` : Request missing parameter
- `404` : Resource not found
- `422` : Wrong info provided
- `405` : Method not allowed

## Testing
To run the tests, run
```
createdb trivia_test
dropdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```