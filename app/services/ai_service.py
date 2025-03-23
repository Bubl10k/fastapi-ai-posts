from google import genai

from app.common.exc.expetion import ValidationError
from app.common.settings import settings

client = genai.Client(api_key=settings.gemini.GEMINI_API_KEY)


class AIService:
    @staticmethod
    def is_content_appropriate(content: str) -> str:
        """
        Checks if the content is appropriate.
        """

        prompt = (
            "Analyze the following text for offensive language, hate speech, threats, or explicit content. "
            "Return 'valid' if the text is appropriate, otherwise return 'blocked'.\n\n"
            f"Text: {content}"
        )

        try:
            response = client.models.generate_content(
                model=settings.gemini.GEMINI_MODEL,
                contents=prompt,
            )

            result = response.text.strip().lower()

            return result
        except Exception as e:
            raise ValidationError(f"AI service error: {e}")

    @staticmethod
    def create_response_text_to_comment(content: str) -> str:
        """
        Creates a response text to a comment.
        """

        prompt = (
            "Generate a response to the following comment. "
            "Your response should be short and concise, and should not exceed 100 characters.\n\n"
            f"Comment: {content}"
        )

        try:
            response = client.models.generate_content(
                model=settings.gemini.GEMINI_MODEL,
                contents=prompt,
            )

            result = response.text.strip().lower()

            return result
        except Exception as e:
            raise ValidationError(f"AI service error: {e}")


def get_ai_service() -> AIService:
    return AIService()
