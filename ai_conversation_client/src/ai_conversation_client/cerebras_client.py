"""Cerebras implementation of the AI Conversation Client interface.

This module implements the AIConversationClient interface for the Cerebras API.
"""

import json
import os
from typing import Any, Optional

import requests

from .api import AIConversationClient


class CerebrasClient(AIConversationClient):
    """Cerebras implementation of the AIConversationClient interface."""

    API_BASE_URL = "https://api.cerebras.ai/v1"

    AVAILABLE_MODELS = [
        {
            "id": "llama-4-scout-17b-16e-instruct",
            "name": "Llama 4 Scout",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "August 2024",
        },
        {
            "id": "llama3.1-8b",
            "name": "Llama 3.1 8B",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "March 2023",
        },
    ]

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize a new Cerebras AI conversation client instance."""
        self.api_key = api_key or os.environ.get("CEREBRAS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Cerebras API key must be provided either as a parameter or "
                "via the CEREBRAS_API_KEY environment variable."
            )

        self._sessions: dict[str, dict[str, Any]] = {}
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def summarize_conversation(self, session_id: str) -> str:
        """Generate summary of the entire conversation."""
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        session = self._sessions[session_id]
        if len(session["history"]) < 2:
            return "Not enough conversation to summarize."

        conversation_text = "\n\n".join(
            f"{'User' if msg['sender'] == 'user' else 'AI'}: {msg['content']}"
            for msg in session["history"]
        )

        messages = [
            {"role": "system", "content": "Please provide a concise summary of the following conversation:"},
            {"role": "user", "content": conversation_text},
        ]

        url = f"{self.API_BASE_URL}/chat/completions"
        payload = {
            "model": session["model"],
            "messages": messages,
            "max_tokens": 256,
        }

        try:
            response = requests.post(url, headers=self._headers, json=payload)
            response.raise_for_status()

            response_data = response.json()
            summary = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not isinstance(summary, str):
                raise ValueError("Invalid response format from API")
            return summary

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to summarize conversation: {str(e)}")

    def export_chat_history(self, session_id: str, format: str = "json") -> str:
        """Export chat history to a specified format."""
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        history = self._sessions[session_id]["history"]

        if format.lower() == "json":
            export_data = {
                "session_id": session_id,
                "user_id": self._sessions[session_id]["user_id"],
                "model": self._sessions[session_id]["model"],
                "created_at": self._sessions[session_id]["created_at"].isoformat(),
                "messages": [
                    {
                        "id": msg["id"],
                        "content": msg["content"],
                        "sender": msg["sender"],
                        "timestamp": msg["timestamp"].isoformat(),
                    }
                    for msg in history
                ],
            }
            return json.dumps(export_data, indent=2)

        elif format.lower() == "txt":
            output = f"Session ID: {session_id}\n"
            output += f"User ID: {self._sessions[session_id]['user_id']}\n"
            output += f"Model: {self._sessions[session_id]['model']}\n"
            output += f"Created: {self._sessions[session_id]['created_at'].isoformat()}\n\n"
            output += "Conversation:\n\n"

            for msg in history:
                sender = "User" if msg["sender"] == "user" else "AI"
                time_str = msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                output += f"[{time_str}] {sender}: {msg['content']}\n\n"

            return output

        else:
            raise ValueError(f"Unsupported export format: {format}. Supported formats: json, txt")

    def switch_model(self, session_id: str, model_id: str) -> bool:
        """Change the AI model for an active session."""
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        available_model_ids = [m["id"] for m in self.AVAILABLE_MODELS]
        if model_id not in available_model_ids:
            raise ValueError(
                f"Model {model_id} is not available. "
                f"Available models: {', '.join(available_model_ids)}"
            )

        self._sessions[session_id]["model"] = model_id
        return True
