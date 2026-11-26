"""
Unit & Integration Tests for Asperion Teams, Internal Communications & Sentinel AI Bot
Tests channels, messaging, document embeds, reactions, pinning, team presence, virtual huddles & Sentinel Bot.
"""
import pytest
from datetime import datetime
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.communications import (
    get_communications_overview, list_channels, create_channel,
    get_channel_messages, post_channel_message, toggle_message_reaction,
    toggle_pin_message, list_team_presence, update_user_presence,
    start_huddle, huddle_action, execute_bot_command
)
from app.schemas.communications import (
    ChannelCreate, MessageCreate, MessageReactionUpdate, PresenceUpdate,
    HuddleStartRequest, HuddleActionRequest, SentinelBotCommandRequest
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_communications_overview(db):
    """Verify aggregated communications overview metrics."""
    ov = get_communications_overview(db=db)
    assert ov.total_channels >= 8
    assert ov.total_messages >= 10
    assert ov.active_presence_count >= 5
    assert ov.online_count >= 1

def test_channels_listing_and_creation(db):
    """Test channel listing and creation with automatic welcome bot message."""
    channels = list_channels(db=db)
    assert len(channels) >= 8
    slugs = [c.slug for c in channels]
    assert "announcements" in slugs
    assert "engineering-devops" in slugs

    # Create new channel
    ts = int(datetime.now().timestamp())
    ch_in = ChannelCreate(
        name=f"frontend-uiux-{ts}",
        display_name=f"🎨 Frontend & UI/UX Guild {ts}",
        description="Design system, micro-interactions, responsive styling.",
        channel_type="PUBLIC_CHANNEL",
        topic="Design tokens and accessibility"
    )
    new_ch = create_channel(channel_in=ch_in, db=db)
    assert new_ch.id is not None
    assert new_ch.slug == f"frontend-uiux-{ts}"
    assert "🎨 Frontend" in new_ch.display_name

    # Check auto welcome message in new channel
    messages = get_channel_messages(channel_id=new_ch.id, db=db)
    assert len(messages) >= 1
    assert "Asperion Sentinel AI Bot" in messages[0].sender_name
    assert "Welcome" in messages[0].content

def test_message_posting_and_document_embed(db):
    """Test posting rich text message and document embed."""
    channels = list_channels(db=db)
    ch = [c for c in channels if c.slug == "engineering-devops"][0]

    # Post standard message
    msg_in = MessageCreate(
        content="Testing high-throughput API gateway response times under load.",
        message_type="TEXT",
        sender_name="Siddharth Kulkarni",
        sender_email="siddharth.kulkarni@asperion.in",
        sender_role="Staff Platform Engineer"
    )
    posted = post_channel_message(channel_id=ch.id, msg_in=msg_in, db=db)
    assert posted.id is not None
    assert posted.channel_id == ch.id
    assert "Testing high-throughput" in posted.content

    # Post document embed message
    doc_in = MessageCreate(
        content="Attached official Purchase Order for AWS Cloud Reserved Instances.",
        message_type="DOCUMENT_EMBED",
        embed_type="PURCHASE_ORDER",
        embed_id=1,
        embed_title="PO-2026-001: AWS Cloud Multi-Region Cluster",
        embed_url="/api/v1/procurement/orders/1/html",
        sender_name="Director Varadi Vijay"
    )
    posted_doc = post_channel_message(channel_id=ch.id, msg_in=doc_in, db=db)
    assert posted_doc.embed_type == "PURCHASE_ORDER"
    assert posted_doc.embed_id == 1
    assert "AWS Cloud" in posted_doc.embed_title

def test_sentinel_bot_automated_trigger(db):
    """Test that posting /kpi or /status in a channel triggers an automated Sentinel Bot reply."""
    channels = list_channels(db=db)
    ch = channels[0]

    initial_msgs = get_channel_messages(channel_id=ch.id, db=db)
    initial_count = len(initial_msgs)

    # Post bot command
    msg_in = MessageCreate(
        content="/status",
        sender_name="Director Varadi Vijay",
        sender_email="director@asperion.in",
        sender_role="Director & Founder"
    )
    post_channel_message(channel_id=ch.id, msg_in=msg_in, db=db)

    # Channel should now have 2 new messages: the user message + the Sentinel Bot reply
    updated_msgs = get_channel_messages(channel_id=ch.id, db=db)
    assert len(updated_msgs) == initial_count + 2
    bot_reply = updated_msgs[-1]
    assert bot_reply.sender_name == "Asperion Sentinel AI Bot"
    assert "Sentinel Enterprise Health" in bot_reply.content
    assert "ISO" in bot_reply.content

def test_reactions_and_pinning(db):
    """Test message reactions and pin toggling."""
    channels = list_channels(db=db)
    ch = channels[0]
    messages = get_channel_messages(channel_id=ch.id, db=db)
    msg = messages[0]

    # Toggle reaction
    react_res = toggle_message_reaction(
        message_id=msg.id,
        payload=MessageReactionUpdate(emoji="🚀", user_name="Director Varadi Vijay"),
        db=db
    )
    assert "🚀" in react_res.reactions
    assert "Director Varadi Vijay" in react_res.reactions["🚀"]

    # Toggle again to remove reaction
    react_res2 = toggle_message_reaction(
        message_id=msg.id,
        payload=MessageReactionUpdate(emoji="🚀", user_name="Director Varadi Vijay"),
        db=db
    )
    assert "🚀" not in react_res2.reactions or "Director Varadi Vijay" not in react_res2.reactions.get("🚀", [])

    # Toggle Pin
    orig_pinned = msg.is_pinned
    pinned_msg = toggle_pin_message(message_id=msg.id, db=db)
    assert pinned_msg.is_pinned == (not orig_pinned)

def test_team_presence_and_status(db):
    """Test presence listing and status updates."""
    presence = list_team_presence(db=db)
    assert len(presence) >= 5
    varad = [p for p in presence if "Varadi Vijay" in p.employee_name][0]
    assert varad.status in ["ONLINE", "IN_MEETING", "FOCUS_DND", "AWAY"]

    # Update status dynamically
    target_status = "IN_MEETING" if varad.status != "IN_MEETING" else "ONLINE"
    upd = update_user_presence(
        payload=PresenceUpdate(status=target_status, status_message="SteerCo Q3 Review", location_tag="Boardroom"),
        user_email="director@asperion.in",
        db=db
    )
    assert upd.status == target_status
    assert upd.status_message == "SteerCo Q3 Review"

def test_virtual_huddle_conference(db):
    """Test starting a virtual huddle, joining, muting, screen sharing, and leaving."""
    channels = list_channels(db=db)
    ch = channels[0]

    # Start huddle
    huddle_req = HuddleStartRequest(
        channel_id=ch.id,
        huddle_title="Urgent SecOps Tabletop Sync",
        started_by_name="Director Varadi Vijay"
    )
    huddle = start_huddle(req=huddle_req, db=db)
    assert huddle.is_active is True
    assert huddle.channel_id == ch.id
    assert len(huddle.participants) >= 1

    # Siddharth joins
    join_res = huddle_action(
        huddle_id=huddle.id,
        req=HuddleActionRequest(action="JOIN", participant_name="Siddharth Kulkarni"),
        db=db
    )
    names = [p["name"] for p in join_res.participants]
    assert "Siddharth Kulkarni" in names

    # Share screen
    screen_res = huddle_action(
        huddle_id=huddle.id,
        req=HuddleActionRequest(action="SHARE_SCREEN", participant_name="Siddharth Kulkarni"),
        db=db
    )
    sidd_p = [p for p in screen_res.participants if p["name"] == "Siddharth Kulkarni"][0]
    assert sidd_p["screen"] is True

    # Leave huddle
    leave_res = huddle_action(
        huddle_id=huddle.id,
        req=HuddleActionRequest(action="LEAVE", participant_name="Siddharth Kulkarni"),
        db=db
    )
    names_after = [p["name"] for p in leave_res.participants]
    assert "Siddharth Kulkarni" not in names_after
