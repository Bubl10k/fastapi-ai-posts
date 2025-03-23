from google import genai

from app.common.exc.expetion import PostValidationError
from app.common.settings import settings


class AIService:
    @staticmethod
    def is_content_appropriate(content: str) -> bool:
        '''
        Checks if the content is appropriate.
        '''
        client = genai.Client(api_key=settings.gemini.GEMINI_API_KEY)

        prompt = (
            "Analyze the following text for offensive language, hate speech, threats, or explicit content. "
            "Return 'POSTED' if the text is appropriate, otherwise return 'BLOCKED'.\n\n"
            f"Text: {content}"
        )

        try:
            response = client.models.generate_content(
                model=settings.gemini.GEMINI_MODEL,
                contents=prompt,
            )

            result = response.text.strip().upper()

            return result == "POSTED"
        except Exception as e:
            raise PostValidationError(f"AI service error: {e}")


def get_ai_service() -> AIService:
    return AIService()
