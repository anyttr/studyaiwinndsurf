import pytest
from datetime import datetime
from src.models.qa import Question, Answer, AnswerComment, QuestionTag, Vote
from src.services.qa_service import QAService
from src.extensions import db

@pytest.fixture
def qa_service():
    return QAService()

@pytest.fixture
def test_user(app):
    from src.models.user import User
    user = User(
        name='Test User',
        email='test@example.com',
        password='password123'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_question(test_user):
    question = Question(
        title='Test Question',
        content='Test content',
        language='en',
        user_id=test_user.id
    )
    tag = QuestionTag(name='python')
    question.tags.append(tag)
    db.session.add(question)
    db.session.commit()
    return question

@pytest.fixture
def test_answer(test_user, test_question):
    answer = Answer(
        content='Test answer',
        user_id=test_user.id,
        question_id=test_question.id
    )
    db.session.add(answer)
    db.session.commit()
    return answer

class TestQAService:
    def test_create_question(self, qa_service, test_user):
        data = {
            'title': 'New Question',
            'content': 'Question content',
            'language': 'en',
            'tags': ['python', 'flask']
        }
        
        question = qa_service.create_question(test_user.id, data)
        
        assert question['title'] == data['title']
        assert question['content'] == data['content']
        assert question['language'] == data['language']
        assert set(question['tags']) == set(data['tags'])
        assert question['user']['id'] == test_user.id

    def test_search_questions(self, qa_service, test_question):
        # Test search by query
        results = qa_service.search_questions(query='Test')
        assert len(results['questions']) == 1
        assert results['questions'][0]['id'] == test_question.id

        # Test search by tag
        results = qa_service.search_questions(tags=['python'])
        assert len(results['questions']) == 1
        assert results['questions'][0]['id'] == test_question.id

        # Test search by language
        results = qa_service.search_questions(language='en')
        assert len(results['questions']) == 1
        assert results['questions'][0]['id'] == test_question.id

    def test_get_question_details(self, qa_service, test_question):
        question = qa_service.get_question_details(test_question.id)
        
        assert question['id'] == test_question.id
        assert question['title'] == test_question.title
        assert question['content'] == test_question.content
        assert question['view_count'] == 1  # Should increment view count

    def test_create_answer(self, qa_service, test_user, test_question):
        data = {
            'content': 'New answer'
        }
        
        answer = qa_service.create_answer(test_user.id, test_question.id, data)
        
        assert answer['content'] == data['content']
        assert answer['user']['id'] == test_user.id
        
        # Check question's answer count
        question = Question.query.get(test_question.id)
        assert question.answer_count == 1

    def test_add_comment(self, qa_service, test_user, test_answer):
        comment = qa_service.add_comment(
            test_user.id,
            test_answer.id,
            'Test comment'
        )
        
        assert comment['content'] == 'Test comment'
        assert comment['user']['id'] == test_user.id

    def test_vote(self, qa_service, test_user, test_question):
        # Test upvote
        result = qa_service.vote(test_user.id, 'question', test_question.id, 1)
        assert result['score'] == 1

        # Test changing vote
        result = qa_service.vote(test_user.id, 'question', test_question.id, -1)
        assert result['score'] == -1

        # Test removing vote
        result = qa_service.vote(test_user.id, 'question', test_question.id, -1)
        assert result['score'] == 0

    def test_accept_answer(self, qa_service, test_user, test_answer):
        # Create another answer
        another_answer = Answer(
            content='Another answer',
            user_id=test_user.id,
            question_id=test_answer.question_id,
            is_accepted=True
        )
        db.session.add(another_answer)
        db.session.commit()

        # Accept the test answer
        result = qa_service.accept_answer(test_user.id, test_answer.id)
        
        assert result['is_accepted'] is True
        
        # Check that the other answer is no longer accepted
        another_answer = Answer.query.get(another_answer.id)
        assert another_answer.is_accepted is False

    def test_get_trending_tags(self, qa_service, test_question):
        tags = qa_service.get_trending_tags()
        
        assert len(tags) > 0
        assert any(tag[0] == 'python' for tag in tags)

    def test_error_handling(self, qa_service, test_user):
        # Test invalid question ID
        with pytest.raises(Exception):
            qa_service.get_question_details(999)

        # Test invalid vote value
        with pytest.raises(ValueError):
            qa_service.vote(test_user.id, 'question', 1, 2)

        # Test accepting answer without permission
        with pytest.raises(ValueError):
            qa_service.accept_answer(999, 1)  # Wrong user ID
