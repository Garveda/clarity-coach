"""
Session Manager for Self Clarity and Business Clarity
File-based session management for storing user progress across sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path(__file__).parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)


class SessionManager:
    """Manages user sessions with file-based storage"""

    def __init__(self, domain: str):
        """
        Initialize session manager for a specific domain

        Args:
            domain: 'self_clarity' or 'business_clarity'
        """
        self.domain = domain
        self.domain_dir = SESSIONS_DIR / domain
        self.domain_dir.mkdir(exist_ok=True)

    def _get_user_file(self, user_id: str) -> Path:
        """Get the file path for a user's session data"""
        return self.domain_dir / f"{user_id}.json"

    def get_session(self, user_id: str) -> dict:
        """
        Get session data for a user

        Returns:
            dict: Session data or empty structure if new user
        """
        user_file = self._get_user_file(user_id)

        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Return empty session structure
        if self.domain == 'self_clarity':
            return {
                "user_id": user_id,
                "domain": "self_clarity",
                "session_count": 0,
                "created_at": datetime.now().isoformat(),
                "last_session": None,
                "key_insights": [],
                "recurring_themes": [],
                "contradictions": [],
                "next_session_focus": "Start with flow moments and energy sources"
            }
        else:  # business_clarity
            return {
                "user_id": user_id,
                "domain": "business_clarity",
                "session_count": 0,
                "created_at": datetime.now().isoformat(),
                "last_session": None,
                "business_context": {},
                "decisions_discussed": [],
                "next_focus": "Understand business core"
            }

    def save_session(self, user_id: str, session_data: dict):
        """
        Save session data for a user

        Args:
            user_id: User identifier
            session_data: Complete session data to save
        """
        session_data["last_session"] = datetime.now().isoformat()

        user_file = self._get_user_file(user_id)
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

    def update_session(self, user_id: str, updates: dict):
        """
        Update specific fields in session data

        Args:
            user_id: User identifier
            updates: Dictionary of fields to update
        """
        session = self.get_session(user_id)
        session.update(updates)
        self.save_session(user_id, session)

    def increment_session(self, user_id: str):
        """Increment session count and return new count"""
        session = self.get_session(user_id)
        session['session_count'] += 1
        self.save_session(user_id, session)
        return session['session_count']

    def add_insight(self, user_id: str, insight: dict):
        """
        Add a new insight to session (Self Clarity)

        Args:
            insight: {
                "session": 1,
                "insight": "User finds fulfillment in...",
                "confidence": 0.8,
                "examples": [...]
            }
        """
        session = self.get_session(user_id)
        session['key_insights'].append(insight)
        self.save_session(user_id, session)

    def list_users(self):
        """List all users with sessions"""
        return [f.stem for f in self.domain_dir.glob("*.json")]

    def delete_session(self, user_id: str):
        """Delete a user's session (for testing/reset)"""
        user_file = self._get_user_file(user_id)
        if user_file.exists():
            user_file.unlink()
            return True
        return False


# Convenience functions
def get_self_clarity_session(user_id: str = "default") -> dict:
    """Get Self Clarity session for a user"""
    manager = SessionManager("self_clarity")
    return manager.get_session(user_id)


def save_self_clarity_session(user_id: str, session_data: dict):
    """Save Self Clarity session"""
    manager = SessionManager("self_clarity")
    manager.save_session(user_id, session_data)


def get_business_clarity_session(user_id: str = "default") -> dict:
    """Get Business Clarity session for a user"""
    manager = SessionManager("business_clarity")
    return manager.get_session(user_id)


def save_business_clarity_session(user_id: str, session_data: dict):
    """Save Business Clarity session"""
    manager = SessionManager("business_clarity")
    manager.save_session(user_id, session_data)
