import os
from typing import Optional, Tuple, List
import time

import requests


class DeepSeekClient:
    """
    HTTP client for DeepSeek API.
    Responsible for calling the model and returning natural-language messages.
    """

    def __init__(self) -> None:
        self._api_key = os.getenv("DEEPSEEK_API_KEY")
        self._base_url = "https://openrouter.ai/api/v1/chat/completions"
        # Allow overriding the model from environment if needed
        self._model_name = os.getenv(
            "DEEPSEEK_MODEL_NAME", "deepseek/deepseek-chat-v3-0324:free"
        )

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

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self._base_url,
                    headers=self._build_headers(),
                    json=body,
                    timeout=30,  # Increased timeout to 30 seconds
                )

                # Handle 429 and 502 errors with retry
                if response.status_code in [429, 502, 503]:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** (attempt + 3)  # 8s, 16s, 32s
                        error_msg = {
                            429: "Rate limit",
                            502: "Bad gateway",
                            503: "Service unavailable",
                        }.get(response.status_code, "Server error")
                        time.sleep(wait_time)
                        continue
                    else:
                        return (
                            None,
                            f"Service temporarily unavailable (status {response.status_code}). Please try again later.",
                        )

                # Handle other non-200 status codes
                if response.status_code != 200:
                    error_detail = response.text
                    return (
                        None,
                        f"OpenRouter returned status code {response.status_code}: {error_detail}",
                    )

                # Success - break out of retry loop
                break

            except requests.RequestException as exc:
                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)
                    print(f"Request failed: {exc}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                return (
                    None,
                    f"OpenRouter request failed after {max_retries} attempts: {str(exc)}",
                )

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError) as exc:
            return None, f"DeepSeek response could not be parsed: {str(exc)}"

        return str(content), None
