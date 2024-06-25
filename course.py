import json

class Course:
    def __init__(self, json_data):
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

    def get_levels(self):
        return list(self.data.keys())

    def get_topics(self, level):
        if level in self.data:
            return [list(topic.keys())[0] for topic in self.data[level]]
        else:
            return None

    def get_lessons(self, level, topic):
        if level in self.data:
            for topic_data in self.data[level]:
                if topic in topic_data:
                    return topic_data[topic]
        return None

    def display_course_structure(self):
        for level in self.data:
            print(f"Level: {level}")
            for topic_data in self.data[level]:
                topic = list(topic_data.keys())[0]
                print(f"  Topic: {topic}")
                for lesson in topic_data[topic]:
                    print(f"    Lesson: {lesson}")

    def get_lesson_for_topic(self, level, topic):
        lessons = self.get_lessons(level, topic)
        if lessons:
            return lessons
        return None
