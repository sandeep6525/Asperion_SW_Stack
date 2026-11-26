"""
Unit & Integration Tests for Enterprise Auto-Fixing Engine and Auto-Update Daemon
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.engines.autofix_engine import run_enterprise_auto_fix_and_self_heal
from app.engines.autoupdate_manager import auto_update_manager
from app.api.system_health import get_system_health, trigger_self_heal

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    yield session
    session.close()

def test_enterprise_auto_fix_dry_run(db):
    res = run_enterprise_auto_fix_and_self_heal(db, dry_run=True)
    assert res["status"] == "HEALTHY"
    assert res["modules_scanned"] >= 8
    assert res["system_health_score"] >= 80.0
    assert "timestamp" in res
    assert isinstance(res["actions_taken"], list)

def test_enterprise_auto_fix_execution(db):
    res = run_enterprise_auto_fix_and_self_heal(db, dry_run=False)
    assert res["status"] == "HEALTHY"
    assert "anomalies_detected" in res
    assert "anomalies_auto_fixed" in res

def test_autoupdate_daemon_lifecycle():
    auto_update_manager.start(interval_seconds=5)
    status = auto_update_manager.get_status()
    assert status["status"] == "RUNNING"
    assert status["interval_seconds"] == 5
    auto_update_manager.stop()
    status_stopped = auto_update_manager.get_status()
    assert status_stopped["status"] == "STOPPED"

def test_api_system_health_endpoint(db):
    health = get_system_health(db=db)
    assert health["status"] == "OPERATIONAL"
    assert "system_health_score" in health
    assert "daemon" in health
    assert "diagnostics" in health
