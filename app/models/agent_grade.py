# coding=utf8
from app.models.base import *


class AgentGrade(Base):
    __tablename__ = 'agt_agent_grades'
    grade_code = db.Column(db.String(20), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    grade_title = db.Column(db.String(20), nullable=False)
