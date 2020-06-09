import random

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    paged_questions = formatted_questions[start:end]

    return paged_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Fetches a list of categories
    @app.route('/categories')
    def get_categories():

        categories = Category.query.all()

        formatted_categories = {}

        for category in categories:
            formatted_categories[f'{category.id}'] = f'{category.type}'

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    # Fetches a list of paginated questions, where each page contains 10
    @app.route('/questions')
    def get_questions():

        questions = Question.query.all()
        paginated_questions = paginate_questions(request, questions)

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': None,
            'categories': formatted_categories
        })

    # Deletes the provided question id and returns a list of paginated questions
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            questions = Question.query.all()
            paginated_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': paginated_questions,
                'total_questions': len(questions)
            })

        except:
            abort(422)

    # Creates a question from request's json body and returns a list of paginated questions
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        try:
            question = Question(
                question=body.get('question', None),
                answer=body.get('answer', None),
                category=body.get('category', None),
                difficulty=body.get('difficulty', None)
            )
            question.insert()

            questions = Question.query.all()
            paginated_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': paginated_questions,
                'total_questions': len(questions)
            })

        except:
            abort(422)

    # Fetches a list of paginated questions based on the provided search term using form
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.form['search_term']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if not len(questions):
            abort(422)

        paginated_questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
        })

    # Fetches a list of paginated questions based on the provided Category Type using request variable
    @app.route('/categories/<category_type>/questions', methods=['POST'])
    def get_questions_by_category(category_type):
        questions = Question.query.filter(Question.category.ilike(category_type)).all()

        if not len(questions):
            abort(422)

        paginated_questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions)
        })

    # Fetches a single question to play the quiz
    @app.route('/play', methods=['POST'])
    def play():
        body = request.get_json()

        previous_questions = body['previous_questions']
        previous_questions_ids = []
        for question in previous_questions:
            previous_questions_ids.append(question.id)

        category_id = body["quiz_category"]["id"]

        if category_id == 0:

            if previous_questions is not None:

                questions = Question.query.filter(Question.id.notin_(previous_questions_ids)).all()

            else:

                questions = Question.query.all()

        else:

            category = Category.query.get(category_id)

            if previous_questions is not None:

                questions = Question.query. \
                    filter(
                    Question.id.notin_(previous_questions_ids),
                    Question.category == category_id) \
                    .all()

            else:

                questions = Question.query.filter(Question.category == category.id).all()

        random_question = random.choice(questions).format()

        return jsonify({
            'success': True,
            'question': random_question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad_request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method_not_allowed"
        }), 405

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
