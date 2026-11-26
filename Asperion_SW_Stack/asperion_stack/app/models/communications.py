"""
Asperion Enterprise OS - Internal Communication System (Teams, Enterprise Chat & Virtual Huddles)
Enterprise-grade messaging, channels, direct messages, document embeds, Sentinel AI Bot, and virtual huddles.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class ChatChannel(Base):
    """
    Enterprise communication channel or direct message thread.
    Types: PUBLIC_CHANNEL, PRIVATE_CHANNEL, DIRECT_MESSAGE, WAR_ROOM
    """
    __tablename__ = "chat_channels"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False) # e.g. 'announcements', 'engineering-devops'
    display_name = Column(String(120), nullable=False) # e.g. '📢 Announcements & Townhall'
    description = Column(String(255), nullable=True)
    channel_type = Column(String(30), default="PUBLIC_CHANNEL", index=True) # PUBLIC_CHANNEL, PRIVATE_CHANNEL, DIRECT_MESSAGE, WAR_ROOM
    topic = Column(String(255), nullable=True)
    is_pinned = Column(Boolean, default=False)
    created_by_name = Column(String(100), default="Director Varadi Vijay")
    unread_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    """
    Individual chat message within a channel or DM.
    Supports rich text, code snippets, document embeds, threading, and emoji reactions.
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("chat_channels.id"), index=True, nullable=False)
    
    sender_id = Column(Integer, nullable=True)
    sender_name = Column(String(100), nullable=False)
    sender_email = Column(String(120), nullable=False)
    sender_role = Column(String(80), default="Team Member")
    sender_avatar = Column(String(255), nullable=True)
    
    content = Column(Text, nullable=False)
    message_type = Column(String(30), default="TEXT", index=True) # TEXT, SYSTEM_BOT, CODE_SNIPPET, DOCUMENT_EMBED, INCIDENT_ALERT
    
    # Optional Document Attachment / Embed
    embed_type = Column(String(50), nullable=True) # OFFER_LETTER, PURCHASE_ORDER, INCIDENT_WAR_ROOM, PAYSLIP, BOARD_RESOLUTION
    embed_id = Column(Integer, nullable=True)
    embed_title = Column(String(255), nullable=True)
    embed_url = Column(String(255), nullable=True)
    
    parent_id = Column(Integer, nullable=True) # For threaded replies
    is_pinned = Column(Boolean, default=False)
    reactions_json = Column(Text, default="{}") # e.g. {"👍": ["Varadi Vijay", "Siddharth"], "🚀": ["Arun"]}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TeamMemberPresence(Base):
    """
    Live presence, availability, and activity status of team members.
    Status: ONLINE, IN_MEETING, AWAY, FOCUS_DND, OFFLINE
    """
    __tablename__ = "team_member_presence"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=True, index=True)
    employee_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    designation = Column(String(100), nullable=False)
    department = Column(String(60), default="Engineering")
    
    status = Column(String(30), default="ONLINE", index=True) # ONLINE, IN_MEETING, AWAY, FOCUS_DND, OFFLINE
    status_message = Column(String(200), default="Available")
    location_tag = Column(String(100), default="Horamavu Bangalore HQ") # Horamavu Bangalore HQ, Remote / WFH, Client Onsite
    avatar_color = Column(String(30), default="blue")
    
    last_active_at = Column(DateTime, default=datetime.utcnow)

class VirtualHuddleSession(Base):
    """
    Real-time audio/video screen-share conference huddle in a channel.
    """
    __tablename__ = "virtual_huddle_sessions"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("chat_channels.id"), index=True, nullable=False)
    channel_name = Column(String(120), nullable=False)
    huddle_title = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    started_by_name = Column(String(100), nullable=False)
    participants_json = Column(Text, default="[]") # JSON list of participant names & mic/cam status
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
