import os
from typing import Optional, Tuple, List

import requests


class DeepSeekClient:
    """
    HTTP client for DeepSeek API.
    Responsible for calling the model and returning natural-language messages.
    """

    def __init__(self) -> None:
        self._api_key = os.getenv("DEEPSEEK_API_KEY")
        self._base_url = "https://api.deepseek.com/v1/chat/completions"
        # Allow overriding the model from environment if needed
        self._model_name = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

    def _build_headers(self) -> dict:
        """
        Build HTTP headers for DeepSeek requests
        """
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _is_configured(self) -> bool:
        """
        Check whether the client has the API key available
        """
        return bool(self._api_key)

    def get_natural_substitute_message(
        self,
        ingredient_name: str,
        categories: List[str],
        current_substitutes: List[str],
        language: str = "es",
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Ask DeepSeek for a friendly message suggesting substitutes.

        """
        if not self._is_configured():
            return None, "DeepSeek API key is not configured"

        system_message = (
            "You are an assistant that suggests ingredient substitutions for home cooking. "
            "Answer with a short, friendly paragraph, directly addressing the user. "
            "Do not add bullet points or Markdown formatting. Just plain text."
        )

        if language == "es":
            user_message = (
                "Sugiere sustitutos de cocina para el siguiente ingrediente.\n"
                f"Ingrediente: {ingredient_name}.\n"
                f"Categorías: {categories}.\n"
                f"Sustitutos ya registrados en el sistema: {current_substitutes}.\n"
                "Responde en español sencillo, con un tono amistoso, como si ayudaras a una persona que cocina en casa. "
                "Incluye entre 3 y 6 posibles sustitutos y comenta brevemente en qué casos funcionan mejor."
            )
        else:
            user_message = (
                "Suggest cooking substitutes for the following ingredient.\n"
                f"Ingredient: {ingredient_name}.\n"
                f"Categories: {categories}.\n"
                f"Substitutes already registered in the system: {current_substitutes}.\n"
                "Use a friendly tone and include 3 to 6 substitutes, briefly describing when they work best."
            )

        body = {
            "model": self._model_name,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 256,
            "temperature": 0.7,
            "stream": False,
        }

        try:
            response = requests.post(
                self._base_url,
                headers=self._build_headers(),
                json=body,
                timeout=15,
            )
        except requests.RequestException as exc:
            return None, f"DeepSeek request failed: {str(exc)}"

        if response.status_code != 200:
            return None, f"DeepSeek returned status code {response.status_code}"

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError) as exc:
            return None, f"DeepSeek response could not be parsed: {str(exc)}"

        return str(content), None
