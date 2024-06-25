import json
import google.generativeai as genai
from secureKey import GEMENI_API_KEY
from course_generator import Course

class CourseGenerator:
    def __init__(self, api_key, model_name='gemini-1.5-flash'):
        self.api_key = api_key
        self.model_name = model_name
        self.configure_genai()

    def configure_genai(self):
        """Configure the generative AI API."""
        genai.configure(api_key=self.api_key)

    def get_gemini_models(self):
        """List available Gemini models that support content generation."""
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(model.name)

    def generate_course_content(self, topic):
        """Generate course content for a given topic."""
        model = genai.GenerativeModel(self.model_name)
        prompt = (
            f'''Give me the topics for learning {topic}.
               Return them as JSON with major topics as the attributes and minor topics as list values.
               Example: {{"Level": [{{"Main Topic 1": ["minor topic1", "minor topic2"]}}]}}.
               The return should be in JSON format and only JSON. No additional text or explanations.'''
        )
        response = model.generate_content(prompt)

        # Print the response text for debugging
        print("Response text from Generative AI:")
        print(response.text)
        
        # Attempt to create a Course instance and display the structure
        try:
            course = Course(response.text)
            course.display_course_structure()
        except ValueError as e:
            print(f"Initialization error: {e}")


if __name__ == "__main__":
    # Initialize the CourseGenerator with the API key
    course_generator = CourseGenerator(GEMENI_API_KEY)

    # Optionally list available models
    # course_generator.get_gemini_models()

    # Generate and display the course content for a given topic
    topic = "learnig android in flutter"  # Example topic, can be changed to any other topic
    course_generator.generate_course_content(topic)
