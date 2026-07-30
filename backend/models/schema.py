from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from database.postgres import Base
from datetime import datetime

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False) # e.g., 'ADMIN', 'AUDITOR', 'USER'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)

class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    original_prompt = Column(Text, nullable=False)
    context_retrieved = Column(JSON, nullable=True)
    tools_called = Column(JSON, nullable=True)
    reasoning_steps = Column(JSON, nullable=True)
    
    final_decision = Column(String, nullable=False)
    final_response = Column(Text, nullable=False)
    hash_value = Column(String, nullable=False)

class TokenMapping(Base):
    __tablename__ = "token_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, unique=True, index=True, nullable=False)
    original_value = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AccessAudit(Base):
    __tablename__ = "access_audits"

    id = Column(Integer, primary_key=True, index=True)
    auditor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, nullable=False)
    accessed_at = Column(DateTime, default=datetime.utcnow)
    query_details = Column(String, nullable=False)
