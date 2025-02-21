"""Question and Answer service"""
from datetime import datetime
from sqlalchemy import func, desc
from src.extensions import db
from src.models import Question, Answer, Tag, QuestionVote, AnswerVote

class QAService:
    """Question and Answer service"""
    
    @staticmethod
    def create_question(title, content, language, user_id, tags=None):
        """Create a new question"""
        question = Question(
            title=title,
            content=content,
            language=language,
            user_id=user_id
        )
        
        if tags:
            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                question.tags.append(tag)
        
        db.session.add(question)
        db.session.commit()
        return question
    
    @staticmethod
    def search_questions(query=None, language=None, user_id=None, tags=None, limit=10):
        """Search questions"""
        q = Question.query
        
        if query:
            q = q.filter(Question.title.ilike(f'%{query}%') | Question.content.ilike(f'%{query}%'))
        
        if language:
            q = q.filter(Question.language == language)
        
        if user_id:
            q = q.filter(Question.user_id == user_id)
        
        if tags:
            for tag_name in tags:
                q = q.filter(Question.tags.any(Tag.name == tag_name))
        
        return q.order_by(desc(Question.created_at)).limit(limit).all()
    
    @staticmethod
    def create_answer(content, user_id, question_id):
        """Create a new answer"""
        answer = Answer(
            content=content,
            user_id=user_id,
            question_id=question_id
        )
        db.session.add(answer)
        db.session.commit()
        return answer
    
    @staticmethod
    def vote_question(user_id, question_id, value):
        """Vote on a question"""
        vote = QuestionVote.query.filter_by(user_id=user_id, question_id=question_id).first()
        
        if vote:
            vote.value = value
        else:
            vote = QuestionVote(
                user_id=user_id,
                question_id=question_id,
                value=value
            )
            db.session.add(vote)
        
        db.session.commit()
        return vote
    
    @staticmethod
    def vote_answer(user_id, answer_id, value):
        """Vote on an answer"""
        vote = AnswerVote.query.filter_by(user_id=user_id, answer_id=answer_id).first()
        
        if vote:
            vote.value = value
        else:
            vote = AnswerVote(
                user_id=user_id,
                answer_id=answer_id,
                value=value
            )
            db.session.add(vote)
        
        db.session.commit()
        return vote
