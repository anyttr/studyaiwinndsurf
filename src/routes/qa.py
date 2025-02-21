"""Question and Answer routes"""
from flask import Blueprint, jsonify, request
from src.models.qa import Question, Answer
from src.services.qa_service import QAService
from src.extensions import db

qa_bp = Blueprint('qa', __name__)
qa_service = QAService()

@qa_bp.route('/questions', methods=['POST'])
def create_question():
    """Create a new question"""
    data = request.get_json()
    
    try:
        question = qa_service.create_question(
            title=data['title'],
            content=data['content'],
            language=data['language'],
            tags=data.get('tags', []),
            user_id=request.user.id
        )
        return jsonify(question.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@qa_bp.route('/questions', methods=['GET'])
def search_questions():
    """Search questions"""
    query = request.args.get('query', '')
    language = request.args.get('language', 'en')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    questions = qa_service.search_questions(
        query=query,
        language=language,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'questions': [q.to_dict() for q in questions.items],
        'total': questions.total,
        'pages': questions.pages,
        'current_page': questions.page
    }), 200

@qa_bp.route('/answers', methods=['POST'])
def create_answer():
    """Create a new answer"""
    data = request.get_json()
    
    try:
        answer = qa_service.create_answer(
            content=data['content'],
            question_id=data['question_id'],
            user_id=request.user.id
        )
        return jsonify(answer.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@qa_bp.route('/questions/<int:question_id>/vote', methods=['POST'])
def vote_question(question_id):
    """Vote on a question"""
    data = request.get_json()
    
    try:
        vote = qa_service.vote_question(
            question_id=question_id,
            user_id=request.user.id,
            vote_type=data['vote_type']
        )
        return jsonify(vote.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@qa_bp.route('/answers/<int:answer_id>/vote', methods=['POST'])
def vote_answer(answer_id):
    """Vote on an answer"""
    data = request.get_json()
    
    try:
        vote = qa_service.vote_answer(
            answer_id=answer_id,
            user_id=request.user.id,
            vote_type=data['vote_type']
        )
        return jsonify(vote.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
