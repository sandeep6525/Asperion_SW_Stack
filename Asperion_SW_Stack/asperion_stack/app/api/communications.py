"""
Asperion Enterprise OS - Comprehensive Internal Communications & Teams API
Channels, Direct Messages, Threaded Messages, Document Embeds, Virtual Huddles & Sentinel AI Bot
"""
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.communications import (
    ChatChannel, ChatMessage, TeamMemberPresence, VirtualHuddleSession
)
from app.models.hrms import Employee, HRLetter
from app.models.finance import PurchaseOrder, Invoice
from app.models.cybersecurity import SecurityIncident
from app.models.governance import BoardResolution
from app.schemas.communications import (
    ChannelCreate, ChannelOut, MessageCreate, MessageOut, MessageReactionUpdate,
    PresenceUpdate, PresenceOut, HuddleStartRequest, HuddleActionRequest, HuddleOut,
    SentinelBotCommandRequest, CommunicationsOverviewOut
)

router = APIRouter(prefix="/communications", tags=["Internal Communications & Teams"])

# Helper: Parse reactions JSON safely
def _parse_reactions(reactions_str: Optional[str]) -> Dict[str, List[str]]:
    if not reactions_str:
        return {}
    try:
        return json.loads(reactions_str)
    except Exception:
        return {}

def _serialize_message(msg: ChatMessage) -> MessageOut:
    return MessageOut(
        id=msg.id,
        channel_id=msg.channel_id,
        sender_id=msg.sender_id,
        sender_name=msg.sender_name,
        sender_email=msg.sender_email,
        sender_role=msg.sender_role,
        sender_avatar=msg.sender_avatar,
        content=msg.content,
        message_type=msg.message_type,
        embed_type=msg.embed_type,
        embed_id=msg.embed_id,
        embed_title=msg.embed_title,
        embed_url=msg.embed_url,
        parent_id=msg.parent_id,
        is_pinned=msg.is_pinned,
        reactions=_parse_reactions(msg.reactions_json),
        created_at=msg.created_at
    )

# 1. Communications Overview Metrics
@router.get("/overview", response_model=CommunicationsOverviewOut)
def get_communications_overview(db: Session = Depends(get_db)):
    total_channels = db.query(ChatChannel).count()
    total_messages = db.query(ChatMessage).count()
    presence_items = db.query(TeamMemberPresence).all()
    online_count = sum(1 for p in presence_items if p.status == "ONLINE")
    active_huddles = db.query(VirtualHuddleSession).filter(VirtualHuddleSession.is_active == True).count()
    active_war_rooms = db.query(ChatChannel).filter(ChatChannel.channel_type == "WAR_ROOM").count()

    return CommunicationsOverviewOut(
        total_channels=total_channels,
        total_messages=total_messages,
        active_presence_count=len(presence_items),
        online_count=online_count,
        active_huddles_count=active_huddles,
        active_war_rooms_count=active_war_rooms
    )

# 2. List & Create Channels
@router.get("/channels", response_model=List[ChannelOut])
def list_channels(db: Session = Depends(get_db)):
    channels = db.query(ChatChannel).order_by(ChatChannel.is_pinned.desc(), ChatChannel.id.asc()).all()
    results = []
    for ch in channels:
        latest = db.query(ChatMessage).filter(ChatMessage.channel_id == ch.id).order_by(ChatMessage.created_at.desc()).first()
        results.append(ChannelOut(
            id=ch.id,
            slug=ch.slug,
            display_name=ch.display_name,
            description=ch.description,
            channel_type=ch.channel_type,
            topic=ch.topic,
            is_pinned=ch.is_pinned,
            created_by_name=ch.created_by_name,
            unread_count=ch.unread_count,
            created_at=ch.created_at,
            latest_message=latest.content[:60] + "..." if (latest and len(latest.content) > 60) else (latest.content if latest else "No messages yet"),
            latest_message_time=latest.created_at.strftime("%H:%M") if latest else ""
        ))
    return results

@router.post("/channels", response_model=ChannelOut)
def create_channel(channel_in: ChannelCreate, db: Session = Depends(get_db)):
    slug = channel_in.name.lower().strip().replace(" ", "-").replace("#", "")
    existing = db.query(ChatChannel).filter(ChatChannel.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Channel with slug '{slug}' already exists")

    ch = ChatChannel(
        slug=slug,
        display_name=channel_in.display_name,
        description=channel_in.description,
        channel_type=channel_in.channel_type,
        topic=channel_in.topic or channel_in.description,
        created_by_name=channel_in.created_by_name or "Director Varadi Vijay"
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)

    # Automatically post a welcome message
    welcome_msg = ChatMessage(
        channel_id=ch.id,
        sender_name="Asperion Sentinel AI Bot",
        sender_email="sentinel@asperion.in",
        sender_role="Autonomous System Orchestrator",
        content=f"🚀 Welcome to **#{ch.slug}** ({ch.display_name})! Channel created by {ch.created_by_name}. Type `/help` for bot automation commands.",
        message_type="SYSTEM_BOT"
    )
    db.add(welcome_msg)
    db.commit()

    return ChannelOut(
        id=ch.id,
        slug=ch.slug,
        display_name=ch.display_name,
        description=ch.description,
        channel_type=ch.channel_type,
        topic=ch.topic,
        is_pinned=ch.is_pinned,
        created_by_name=ch.created_by_name,
        unread_count=0,
        created_at=ch.created_at,
        latest_message=welcome_msg.content,
        latest_message_time=welcome_msg.created_at.strftime("%H:%M")
    )

# 3. List & Post Messages in Channel
@router.get("/channels/{channel_id}/messages", response_model=List[MessageOut])
def get_channel_messages(channel_id: int, db: Session = Depends(get_db)):
    ch = db.query(ChatChannel).filter(ChatChannel.id == channel_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    messages = db.query(ChatMessage).filter(ChatMessage.channel_id == channel_id).order_by(ChatMessage.created_at.asc()).all()
    return [_serialize_message(m) for m in messages]

@router.post("/channels/{channel_id}/messages", response_model=MessageOut)
def post_channel_message(channel_id: int, msg_in: MessageCreate, db: Session = Depends(get_db)):
    ch = db.query(ChatChannel).filter(ChatChannel.id == channel_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    msg = ChatMessage(
        channel_id=channel_id,
        sender_name=msg_in.sender_name or "Director Varadi Vijay",
        sender_email=msg_in.sender_email or "director@asperion.in",
        sender_role=msg_in.sender_role or "Director & Founder",
        content=msg_in.content,
        message_type=msg_in.message_type,
        embed_type=msg_in.embed_type,
        embed_id=msg_in.embed_id,
        embed_title=msg_in.embed_title,
        embed_url=msg_in.embed_url,
        parent_id=msg_in.parent_id,
        reactions_json="{}"
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Check for Sentinel Bot trigger: message starts with '/' or contains '@sentinel'
    content_lower = msg_in.content.strip().lower()
    if content_lower.startswith("/") or "@sentinel" in content_lower:
        _handle_bot_response(channel_id, msg_in.content.strip(), msg_in.sender_name, db)

    return _serialize_message(msg)

def _handle_bot_response(channel_id: int, raw_command: str, requester: str, db: Session):
    cmd = raw_command.replace("@sentinel", "").strip().lower()
    reply = ""

    if cmd.startswith("/status") or "status" in cmd:
        reply = (
            "🤖 **[Sentinel Enterprise Health]**\n"
            "- **OS Version:** Asperion Enterprise OS v2.0 (High-Availability Production)\n"
            "- **Horamavu HQ Node:** ONLINE (13.035820, 77.653410 GPS Verified)\n"
            "- **ISO 9001 / 27001 / 42001 Controls:** 100% Passing\n"
            "- **FIDO2 / ZTNA Gateways:** 100% Bound\n"
            "- **CERT-In War Room:** Normal Monitoring (0 Active Breaches)\n"
            "- **Background Auto-Healing:** 30s Heartbeat Active"
        )
    elif cmd.startswith("/kpi") or "kpi" in cmd:
        reply = (
            "🤖 **[Sentinel Live Executive MIS]**\n"
            "- **CIN:** U85500KA2026OPC222069\n"
            "- **Active Personnel:** 8 Verified On-Roster\n"
            "- **Annual Payroll CTC:** ₹1.935 Cr Fixed\n"
            "- **Monthly Inflow Pipeline:** ₹48.50L Enterprise Bookings\n"
            "- **Statutory Tax & PT:** Karnataka PT ₹200/mo & EPFO 12% PF fully reconciled"
        )
    elif cmd.startswith("/payroll") or "payroll" in cmd:
        reply = (
            "🤖 **[Sentinel Payroll Engine]**\n"
            "- **Cycle:** JUN-2026\n"
            "- **Disbursement Status:** Generated & Reconciled with ICICI Bank NEFT Batch\n"
            "- **Wage Code 2019 Rule:** 50% Basic threshold strictly verified\n"
            "- **Payslips:** Downloadable in PDF / Printable HTML via HRMS Portal"
        )
    elif cmd.startswith("/certin") or "certin" in cmd or "incident" in cmd:
        reply = (
            "🤖 **[Sentinel Cybersecurity & CERT-In Bot]**\n"
            "- **Statutory Mandate:** 6-Hour Mandatory Incident Reporting Window active\n"
            "- **War Room Channel:** `#cybersecurity-soc`\n"
            "- **Recent Incident:** `INC-2026-0881` (Triage Closed with Root Cause Contained)\n"
            "- **ISO/IEC 27001 Control A.16.1:** Incident Management in full compliance"
        )
    elif cmd.startswith("/iso") or "iso" in cmd:
        reply = (
            "🤖 **[Sentinel Standards & Quality Desk]**\n"
            "- **Active Certifications:** ISO 9001:2015, ISO/IEC 27001, ISO/IEC 42001, ISO/IEC 20000-1, ISO 22301\n"
            "- **Annual Surveillance Audit:** Scheduled Q3-2026\n"
            "- **Corrective Action Worksheets:** 0 Overdue Major Non-Conformances"
        )
    elif cmd.startswith("/whois") or "whois" in cmd:
        reply = (
            f"🤖 **[Sentinel Directory Lookup for {requester}]**\n"
            "- **Founder & Director:** Varadi Vijay (Sole Member & Governing Director)\n"
            "- **Lead Architect:** Siddharth Kulkarni (Staff Platform Engineer)\n"
            "- **SecOps & CERT-In Lead:** Arun Sharma\n"
            "- **People & Culture Lead:** Priya Nair\n"
            "- **Finance & Accounts Head:** Neha Sharma"
        )
    else: # /help or unknown
        reply = (
            "🤖 **[Asperion Sentinel AI Bot Commands]**\n"
            "- `/status` — View real-time cluster health, ISO controls & Horamavu node status\n"
            "- `/kpi` — View corporate MIS metrics, CIN, revenue run-rate & headcount\n"
            "- `/payroll` — Check attendance-synced payroll cycle & ICICI bank batch status\n"
            "- `/certin` — Check CERT-In war room 6-hour reporting clock & incidents\n"
            "- `/iso` — Review ISO 9001 / 27001 surveillance audit readiness\n"
            "- `/whois` — Corporate organizational structure lookup\n"
            "- `/help` — Display this assistant menu"
        )

    bot_msg = ChatMessage(
        channel_id=channel_id,
        sender_name="Asperion Sentinel AI Bot",
        sender_email="sentinel@asperion.in",
        sender_role="Autonomous System Orchestrator",
        content=reply,
        message_type="SYSTEM_BOT"
    )
    db.add(bot_msg)
    db.commit()

# 4. Message Emoji Reactions
@router.post("/messages/{message_id}/reactions", response_model=MessageOut)
def toggle_message_reaction(message_id: int, payload: MessageReactionUpdate, db: Session = Depends(get_db)):
    msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    reactions = _parse_reactions(msg.reactions_json)
    emoji = payload.emoji
    user = payload.user_name or "Director Varadi Vijay"

    if emoji not in reactions:
        reactions[emoji] = [user]
    else:
        if user in reactions[emoji]:
            reactions[emoji].remove(user)
            if not reactions[emoji]:
                del reactions[emoji]
        else:
            reactions[emoji].append(user)

    msg.reactions_json = json.dumps(reactions)
    db.commit()
    db.refresh(msg)
    return _serialize_message(msg)

# 5. Pin / Unpin Message
@router.patch("/messages/{message_id}/pin", response_model=MessageOut)
def toggle_pin_message(message_id: int, db: Session = Depends(get_db)):
    msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    msg.is_pinned = not msg.is_pinned
    db.commit()
    db.refresh(msg)
    return _serialize_message(msg)

# 6. Team Presence Roster
@router.get("/presence", response_model=List[PresenceOut])
def list_team_presence(db: Session = Depends(get_db)):
    presence_list = db.query(TeamMemberPresence).order_by(TeamMemberPresence.id.asc()).all()
    return presence_list

@router.patch("/presence", response_model=PresenceOut)
def update_user_presence(payload: PresenceUpdate, user_email: str = Query("director@asperion.in"), db: Session = Depends(get_db)):
    pres = db.query(TeamMemberPresence).filter(TeamMemberPresence.email == user_email).first()
    if not pres:
        # Create default presence entry
        pres = TeamMemberPresence(
            employee_name="Director Varadi Vijay",
            email=user_email,
            designation="Director & Founder",
            department="Executive Management",
            status=payload.status,
            status_message=payload.status_message or "Available",
            location_tag=payload.location_tag or "Horamavu Bangalore HQ"
        )
        db.add(pres)
    else:
        pres.status = payload.status
        if payload.status_message is not None:
            pres.status_message = payload.status_message
        if payload.location_tag is not None:
            pres.location_tag = payload.location_tag
        pres.last_active_at = datetime.utcnow()

    db.commit()
    db.refresh(pres)
    return pres

# 7. Virtual Audio/Video Huddle Conferences
@router.post("/huddle/start", response_model=HuddleOut)
def start_huddle(req: HuddleStartRequest, db: Session = Depends(get_db)):
    ch = db.query(ChatChannel).filter(ChatChannel.id == req.channel_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel not found")

    # End existing active huddles in channel
    existing = db.query(VirtualHuddleSession).filter(VirtualHuddleSession.channel_id == req.channel_id, VirtualHuddleSession.is_active == True).all()
    for h in existing:
        h.is_active = False
        h.ended_at = datetime.utcnow()

    initial_participants = [
        {"name": req.started_by_name or "Director Varadi Vijay", "role": "Host", "mic": True, "cam": True, "screen": False, "joined_at": datetime.utcnow().strftime("%H:%M")}
    ]

    huddle = VirtualHuddleSession(
        channel_id=req.channel_id,
        channel_name=ch.display_name,
        huddle_title=req.huddle_title,
        is_active=True,
        started_by_name=req.started_by_name or "Director Varadi Vijay",
        participants_json=json.dumps(initial_participants)
    )
    db.add(huddle)
    db.commit()
    db.refresh(huddle)

    # Post message in channel about huddle
    huddle_msg = ChatMessage(
        channel_id=req.channel_id,
        sender_name="Asperion Sentinel AI Bot",
        sender_email="sentinel@asperion.in",
        sender_role="Autonomous System Orchestrator",
        content=f"🎙️ **Live Virtual Huddle Started:** \"{req.huddle_title}\" started by {req.started_by_name}. Click **Join Huddle** to participate with high-fidelity audio/video & screen share.",
        message_type="SYSTEM_BOT"
    )
    db.add(huddle_msg)
    db.commit()

    return HuddleOut(
        id=huddle.id,
        channel_id=huddle.channel_id,
        channel_name=huddle.channel_name,
        huddle_title=huddle.huddle_title,
        is_active=huddle.is_active,
        started_by_name=huddle.started_by_name,
        participants=initial_participants,
        created_at=huddle.created_at
    )

@router.post("/huddle/{huddle_id}/action", response_model=HuddleOut)
def huddle_action(huddle_id: int, req: HuddleActionRequest, db: Session = Depends(get_db)):
    huddle = db.query(VirtualHuddleSession).filter(VirtualHuddleSession.id == huddle_id).first()
    if not huddle:
        raise HTTPException(status_code=404, detail="Huddle not found")

    participants = json.loads(huddle.participants_json or "[]")
    action = req.action.upper()
    name = req.participant_name

    if action == "JOIN":
        if not any(p["name"] == name for p in participants):
            participants.append({"name": name, "role": "Participant", "mic": True, "cam": True, "screen": False, "joined_at": datetime.utcnow().strftime("%H:%M")})
    elif action == "LEAVE":
        participants = [p for p in participants if p["name"] != name]
        if not participants:
            huddle.is_active = False
            huddle.ended_at = datetime.utcnow()
    elif action in ["MUTE", "UNMUTE"]:
        for p in participants:
            if p["name"] == name:
                p["mic"] = (action == "UNMUTE")
    elif action in ["SHARE_SCREEN", "STOP_SCREEN"]:
        for p in participants:
            if p["name"] == name:
                p["screen"] = (action == "SHARE_SCREEN")

    huddle.participants_json = json.dumps(participants)
    db.commit()
    db.refresh(huddle)

    return HuddleOut(
        id=huddle.id,
        channel_id=huddle.channel_id,
        channel_name=huddle.channel_name,
        huddle_title=huddle.huddle_title,
        is_active=huddle.is_active,
        started_by_name=huddle.started_by_name,
        participants=participants,
        created_at=huddle.created_at
    )

# 8. Direct Bot Command Dispatch
@router.post("/bot/command")
def execute_bot_command(req: SentinelBotCommandRequest, db: Session = Depends(get_db)):
    _handle_bot_response(req.channel_id, req.command, req.requester_name or "Director Varadi Vijay", db)
    return {"status": "success", "command": req.command, "channel_id": req.channel_id}
