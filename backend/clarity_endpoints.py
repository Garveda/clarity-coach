"""
Self Clarity and Business Clarity Endpoints
New endpoints for personal reflection and business consulting
"""

from fastapi import HTTPException, Body
from openai import OpenAI
from datetime import datetime
import json
import os
from dotenv import load_dotenv

import prompts
import session_manager

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def setup_clarity_routes(app):
    """Setup Self Clarity and Business Clarity routes"""

    # ------------------------------
    # Self Clarity Endpoints
    # ------------------------------

    @app.post("/self-clarity")
    async def self_clarity(payload: dict = Body(...)):
        """
        Self Clarity - Personal reflection coach using Socratic method

        Works across multiple sessions (5-10 typically) to help users
        discover patterns, contradictions, and core insights about themselves.
        """
        user_id = payload.get("user_id", "default")
        user_message = payload.get("message", "")

        if not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        try:
            # Get or create session
            manager = session_manager.SessionManager("self_clarity")
            session = manager.get_session(user_id)

            # Increment session count if this is a new session start
            if not session.get('current_conversation'):
                session['session_count'] += 1
                session['current_conversation'] = []

            session_number = session['session_count']

            # Add user message to conversation
            session['current_conversation'].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })

            # Get appropriate prompt for current session number
            system_prompt = prompts.get_self_clarity_prompt(
                session_number=min(session_number, 5),  # Cap at session 5
                question_pattern_type="all"
            )

            # Build conversation context
            conversation_context = ""
            if session['session_count'] > 1:
                conversation_context = f"""
PREVIOUS SESSION INSIGHTS:
{json.dumps(session['key_insights'][-3:], indent=2)}

RECURRING THEMES:
{', '.join(session['recurring_themes'])}

CONTRADICTIONS IDENTIFIED:
{', '.join(session['contradictions'])}

NEXT SESSION FOCUS:
{session['next_session_focus']}
"""

            # Create prompt for OpenAI
            user_prompt = f"""
SESSION {session_number} CONVERSATION

{conversation_context}

USER MESSAGE:
{user_message}

Respond with reflection questions appropriate for Session {session_number}.
Return JSON format:
{{
  "reflection": "Your Socratic question(s) or observation",
  "encouragement": "Encouraging words",
  "session_progress": "Brief note on where we are in the journey"
}}
"""

            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            response_json = json.loads(response.choices[0].message.content)

            # Add AI response to conversation
            session['current_conversation'].append({
                "role": "assistant",
                "content": response_json,
                "timestamp": datetime.now().isoformat()
            })

            # Save session
            manager.save_session(user_id, session)

            return {
                "success": True,
                "session_number": session_number,
                "total_sessions": session['session_count'],
                "reflection": response_json.get("reflection", ""),
                "encouragement": response_json.get("encouragement", ""),
                "session_progress": response_json.get("session_progress", ""),
                "themes": session['recurring_themes'],
                "insights_count": len(session['key_insights'])
            }

        except Exception as e:
            print(f"[ERROR] Self Clarity error: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Self Clarity failed: {str(e)}")

    @app.get("/self-clarity/session/{user_id}")
    async def get_self_clarity_session(user_id: str):
        """Get current session status for a user"""
        manager = session_manager.SessionManager("self_clarity")
        session = manager.get_session(user_id)

        return {
            "user_id": user_id,
            "session_count": session['session_count'],
            "insights_count": len(session['key_insights']),
            "themes": session['recurring_themes'],
            "contradictions": session['contradictions'],
            "next_focus": session['next_session_focus'],
            "last_session": session.get('last_session')
        }

    @app.post("/self-clarity/reset/{user_id}")
    async def reset_self_clarity_session(user_id: str):
        """Reset a user's session (for testing)"""
        manager = session_manager.SessionManager("self_clarity")
        deleted = manager.delete_session(user_id)

        return {
            "success": deleted,
            "message": f"Session reset for user {user_id}" if deleted else "No session found"
        }

    # ------------------------------
    # Business Clarity Endpoints
    # ------------------------------

    @app.post("/business-clarity")
    async def business_clarity(payload: dict = Body(...)):
        """
        Business Clarity - Socratic business consulting

        Helps with automation decisions, process optimization,
        and business strategy through guided questions.
        """
        user_id = payload.get("user_id", "default")
        user_message = payload.get("message", "")
        topic = payload.get("topic", "general")

        if not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        try:
            # Get or create session
            manager = session_manager.SessionManager("business_clarity")
            session = manager.get_session(user_id)

            # Increment session
            session['session_count'] += 1

            # Get business prompt
            system_prompt = prompts.get_business_prompt(question_pattern_type="all")

            # Build context from previous sessions
            context = ""
            if session.get('business_context'):
                context = f"""
BUSINESS CONTEXT (from previous sessions):
{json.dumps(session['business_context'], indent=2)}

DECISIONS DISCUSSED:
{', '.join(session['decisions_discussed'][-3:])}
"""

            # Create prompt
            user_prompt = f"""
BUSINESS CONSULTATION SESSION {session['session_count']}

{context}

TOPIC: {topic}

USER INPUT:
{user_message}

Provide Socratic business guidance appropriate for this stage.
Return JSON format:
{{
  "question": "Your guiding question(s)",
  "insight": "Any observation or reflection to share",
  "next_step": "Suggested next thinking step"
}}
"""

            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            response_json = json.loads(response.choices[0].message.content)

            # Update session
            if topic not in session['decisions_discussed']:
                session['decisions_discussed'].append(topic)

            manager.save_session(user_id, session)

            return {
                "success": True,
                "session_number": session['session_count'],
                "question": response_json.get("question", ""),
                "insight": response_json.get("insight", ""),
                "next_step": response_json.get("next_step", ""),
                "topic": topic
            }

        except Exception as e:
            print(f"[ERROR] Business Clarity error: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Business Clarity failed: {str(e)}")

    @app.get("/business-clarity/session/{user_id}")
    async def get_business_clarity_session(user_id: str):
        """Get current business clarity session status"""
        manager = session_manager.SessionManager("business_clarity")
        session = manager.get_session(user_id)

        return {
            "user_id": user_id,
            "session_count": session['session_count'],
            "decisions_discussed": session['decisions_discussed'],
            "business_context": session['business_context'],
            "next_focus": session['next_focus']
        }

    print("[INFO] Self Clarity and Business Clarity endpoints registered")
