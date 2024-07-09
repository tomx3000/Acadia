import google.generativeai as genai
from secureKey import GEMENI_API_KEY

class GeminiAPIClient:
    def __init__(self, model_name='gemini-1.5-pro'):
        self.api_key = GEMENI_API_KEY
        self.model_name = model_name
        self.configure_genai()

    def configure_genai(self):
        """Configure the generative AI API."""
        genai.configure(api_key=self.api_key)

    def send_prompt(self, prompt):
        """Send a prompt to the Gemini model and return the response."""
        model = genai.GenerativeModel(self.model_name)
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error sending prompt to Gemini API: {e}")
            return None
