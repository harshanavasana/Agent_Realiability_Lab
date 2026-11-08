import json
import httpx
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class OllamaClient(BaseModel):
    model_name: str = "qwen2.5:1.5b"
    base_url: str = "http://localhost:11434/api/chat"
    timeout_seconds: float = 30.0

    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> str:
        """Sends a chat request to local Ollama runtime and returns raw text response."""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
            "format": "json",  # Constrain Ollama sampling engine to output valid JSON syntax
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except httpx.TimeoutException:
            raise RuntimeError(f"Ollama API request timed out after {self.timeout_seconds}s")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Ollama HTTP error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to local Ollama instance: {str(e)}")