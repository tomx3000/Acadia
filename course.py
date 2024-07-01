from gemini_api_client import GeminiAPIClient
import json

gemini_client = GeminiAPIClient()

class Lesson:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.full_content = ""
    
    def generate_full_content(self, level):
        prompt = f"""
        Give me a detailed lesson on {self.title}, {self.content} for learning level {level}.
        """
        response_text = gemini_client.send_prompt(prompt)

        # Print the response text for debugging
        print("Response text from Generative AI:")
        print(response_text)

        self.full_content = response_text

class Levels:
    def __init__(self, title):
        self.title = title
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

class Course:
    def __init__(self, json_data):
        self.levels = []
        if isinstance(json_data, str):
            if json_data.strip() == "":
                raise ValueError("Empty JSON data string")
            try:
                self.data = json.loads(json_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON data: {e}")
                raise
        elif isinstance(json_data, dict):
            self.data = json_data
        else:
            raise ValueError("Invalid JSON data format")

        self._parse_json_data()

    def _parse_json_data(self):
        for level, topics in self.data.items():
            level_obj = Levels(level)
            for topic_data in topics:
                topic = list(topic_data.keys())[0]
                for lesson_data in topic_data[topic]:
                    lesson = Lesson(lesson_data['title'], lesson_data['content'])
                    level_obj.add_lesson(lesson)
            self.levels.append(level_obj)

    def get_levels(self):
        return [level.title for level in self.levels]

    def get_topics(self, level_title):
        level = next((l for l in self.levels if l.title == level_title), None)
        if level:
            return [lesson.title for lesson in level.lessons]
        return None

    def get_lessons(self, level_title, topic_title):
        level = next((l for l in self.levels if l.title == level_title), None)
        if level:
            lesson = next((lesson for lesson in level.lessons if lesson.title == topic_title), None)
            if lesson:
                return lesson.content
        return None

    def display_course_structure(self):
        for level in self.levels:
            print(f"Level: {level.title}")
            for lesson in level.lessons:
                print(f"  Lesson: {lesson.title}")
                print(f"    Content: {lesson.content}")

    def get_lesson_for_topic(self, level_title, topic_title):
        return self.get_lessons(level_title, topic_title)

if __name__ == "__main__":
    # Example JSON data
    json_data = '''
    {
        "Beginner": [
            {
                "Fundamentals": [
                    {
                        "title": "Introduction to Python",
                        "content": "Understanding Python's syntax, data types, variables, and basic operations."
                    },
                    {
                        "title": "Control Flow",
                        "content": "Learning about conditional statements (if-else), loops (for, while), and functions."
                    },
                    {
                        "title": "Data Structures",
                        "content": "Exploring lists, tuples, dictionaries, and sets for organizing and managing data."
                    }
                ]
            },
            {
                "Working with Data": [
                    {
                        "title": "Input and Output",
                        "content": "Getting user input and displaying output using print statements and file handling."
                    },
                    {
                        "title": "String Manipulation",
                        "content": "Learning techniques for working with text, including formatting, slicing, and searching."
                    }
                ]
            }
        ]
    }
    '''

    # Creating a Course object with the example JSON data
    course = Course(json_data)
    course.display_course_structure()

    # Generate detailed content for the first lesson of the first level
    course.levels[0].lessons[0].generate_full_content("Beginner")
    print("\nDetailed Lesson Content:")
    print(course.levels[0].lessons[0].full_content)
