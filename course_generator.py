from course import Course
from gemini_api_client import GeminiAPIClient
import json

class CourseGenerator:
    def __init__(self, model_name='gemini-1.5-flash'):
        self.gemini_client = GeminiAPIClient(model_name)

    def generate_course_content(self, topic):
        """Generate course content for a given topic."""
        prompt = (
            f'''Give me the topics for learning {topic}.
               Return them as JSON with major topics as the attributes and minor topics as list values.
               Example: {{"Level": [{{"Main Topic 1": ["minor topic1", "minor topic2"]}}]}}.
               The return should be in JSON format and only JSON. No additional text or explanations.'''
        )
        response_text = self.gemini_client.send_prompt(prompt)

        # Print the response text for debugging
        print("Response text from Generative AI:")
        print(response_text)
        
        # Attempt to create a Course instance and display the structure
        try:
            course = Course(response_text)
            course.display_course_structure()
            return course
        except ValueError as e:
            print(f"Initialization error: {e}")
            return None

    def generate_lessons_for_topic(self, level, topic):
        """Generate lessons for a specific level and topic."""
        prompt = (
            f'''Generate detailed lessons for the topic "{topic}" under the level "{level}".
               Return them as a JSON list. The return should be in JSON format and only JSON.
               No additional text or explanations.'''
        )
        response_text = self.gemini_client.send_prompt(prompt)

        # Print the response text for debugging
        print("Response text from Generative AI:")
        print(response_text)

        # Attempt to parse the JSON response
        try:
            lessons = json.loads(response_text)
            return lessons
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return None

    def write_to_file(self, filename, topic, course, lessons):
        """Write the course content and lessons to a text file with proper formatting."""
        with open(filename, 'w') as file:
            file.write(f"Course Content for Topic: {topic}\n")
            file.write("=" * 40 + "\n")
            
            for level in course.get_levels():
                file.write(f"Level: {level}\n")
                for topic_data in course.data[level]:
                    topic_name = list(topic_data.keys())[0]
                    file.write(f"  Topic: {topic_name}\n")
                    for lesson in topic_data[topic_name]:
                        file.write(f"    Lesson: {lesson}\n")
            file.write("\n")
            file.write("Detailed Lessons\n")
            file.write("=" * 40 + "\n")
            if lessons:
                for lesson in lessons:
                    file.write(f"  Lesson: {lesson}\n")

if __name__ == "__main__":
    # Initialize the CourseGenerator with the API key
    course_generator = CourseGenerator()

    # Generate and display the course content for a given topic
    topic = "learning python"  # Example topic, can be changed to any other topic
    course = course_generator.generate_course_content(topic)

    # Generate lessons for a specific level and topic
    if course:
        level = "Beginner"  # Example level
        topic = "Introduction"  # Example topic
        lessons = course_generator.generate_lessons_for_topic(level, topic)
        if lessons:
            print(f"Lessons for {topic} in {level}:")
            for lesson in lessons:
                print(f"  Lesson: {lesson}")
        
        # Write everything to a file
        course_generator.write_to_file("course_content.txt", topic, course, lessons)
