"""
Asperion Enterprise OS - Communications & Teams Pydantic Schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChannelCreate(BaseModel):
    name: str # slug, e.g. 'engineering-devops'
    display_name: str
    description: Optional[str] = None
    channel_type: str = "PUBLIC_CHANNEL" # PUBLIC_CHANNEL, PRIVATE_CHANNEL, DIRECT_MESSAGE, WAR_ROOM
    topic: Optional[str] = None
    created_by_name: Optional[str] = "Director Varadi Vijay"

class ChannelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    display_name: str
    description: Optional[str] = None
    channel_type: str
    topic: Optional[str] = None
    is_pinned: bool
    created_by_name: str
    unread_count: int
    created_at: datetime
    latest_message: Optional[str] = None
    latest_message_time: Optional[str] = None

class MessageCreate(BaseModel):
    content: str
    message_type: str = "TEXT" # TEXT, SYSTEM_BOT, CODE_SNIPPET, DOCUMENT_EMBED, INCIDENT_ALERT
    embed_type: Optional[str] = None # OFFER_LETTER, PURCHASE_ORDER, INCIDENT_WAR_ROOM, PAYSLIP, BOARD_RESOLUTION
    embed_id: Optional[int] = None
    embed_title: Optional[str] = None
    embed_url: Optional[str] = None
    parent_id: Optional[int] = None
    sender_name: Optional[str] = "Director Varadi Vijay"
    sender_email: Optional[str] = "director@asperion.in"
    sender_role: Optional[str] = "Director & Founder"

class MessageReactionUpdate(BaseModel):
    emoji: str # e.g. '👍', '🚀', '❤️', '👀', '🎯', '🔥'
    user_name: Optional[str] = "Director Varadi Vijay"

class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    channel_id: int
    sender_id: Optional[int] = None
    sender_name: str
    sender_email: str
    sender_role: str
    sender_avatar: Optional[str] = None
    content: str
    message_type: str
    embed_type: Optional[str] = None
    embed_id: Optional[int] = None
    embed_title: Optional[str] = None
    embed_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_pinned: bool
    reactions: Dict[str, List[str]] = {}
    created_at: datetime

class PresenceUpdate(BaseModel):
    status: str # ONLINE, IN_MEETING, AWAY, FOCUS_DND, OFFLINE
    status_message: Optional[str] = None
    location_tag: Optional[str] = None

class PresenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: Optional[int] = None
    employee_name: str
    email: str
    designation: str
    department: str
    status: str
    status_message: str
    location_tag: str
    avatar_color: str
    last_active_at: datetime

class HuddleStartRequest(BaseModel):
    channel_id: int
    huddle_title: str
    started_by_name: Optional[str] = "Director Varadi Vijay"

class HuddleActionRequest(BaseModel):
    action: str # JOIN, LEAVE, MUTE, UNMUTE, SHARE_SCREEN, STOP_SCREEN
    participant_name: str

class HuddleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    channel_id: int
    channel_name: str
    huddle_title: str
    is_active: bool
    started_by_name: str
    participants: List[Dict[str, Any]] = []
    created_at: datetime

class SentinelBotCommandRequest(BaseModel):
    command: str # e.g. '/help', '/status', '/kpi', '/payroll', '/certin', '/iso'
    channel_id: int
    requester_name: Optional[str] = "Director Varadi Vijay"

class CommunicationsOverviewOut(BaseModel):
    total_channels: int
    total_messages: int
    active_presence_count: int
    online_count: int
    active_huddles_count: int
    active_war_rooms_count: int
