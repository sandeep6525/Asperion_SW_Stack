"""
Asperion Enterprise OS - Background Auto-Update & Autonomous Watcher Daemon
Continuously runs in the background to auto-sync enterprise metrics,
auto-heal anomalies every 60 seconds, and refresh operational state.
"""
import time
import threading
from datetime import datetime
from typing import Dict, Any

from app.database import SessionLocal
from app.engines.autofix_engine import run_enterprise_auto_fix_and_self_heal
from app.engines.notification_engine import scan_and_sync_system_alerts

class AsperionAutoUpdateManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AsperionAutoUpdateManager, cls).__new__(cls)
                cls._instance.is_running = False
                cls._instance.thread = None
                cls._instance.interval_seconds = 30
                cls._instance.last_run_timestamp = None
                cls._instance.total_runs_count = 0
                cls._instance.total_healed_count = 0
                cls._instance.last_report = {}
        return cls._instance

    def start(self, interval_seconds: int = 30):
        if self.is_running:
            return
        self.interval_seconds = interval_seconds
        self.is_running = True
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()
        print(f"[AutoUpdateManager] Background autonomous sync and self-healing started (Interval: {self.interval_seconds}s).")

    def stop(self):
        self.is_running = False
        print("[AutoUpdateManager] Background watcher paused.")

    def _worker_loop(self):
        while self.is_running:
            try:
                db = SessionLocal()
                # 1. Run Automated Alert Scan
                scan_and_sync_system_alerts(db)

                # 2. Run Enterprise Auto-Fix and Self-Healing
                report = run_enterprise_auto_fix_and_self_heal(db)

                self.last_run_timestamp = datetime.now()
                self.total_runs_count += 1
                self.total_healed_count += report.get("anomalies_auto_fixed", 0)
                self.last_report = report

                db.close()
            except Exception as e:
                print(f"[AutoUpdateManager Error] {e}")

            # Sleep in small slices to allow graceful shutdown
            for _ in range(self.interval_seconds):
                if not self.is_running:
                    break
                time.sleep(1)

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "RUNNING" if self.is_running else "STOPPED",
            "interval_seconds": self.interval_seconds,
            "last_run": self.last_run_timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.last_run_timestamp else None,
            "total_runs": self.total_runs_count,
            "total_healed_cumulative": self.total_healed_count,
            "latest_diagnostics": self.last_report
        }

auto_update_manager = AsperionAutoUpdateManager()
