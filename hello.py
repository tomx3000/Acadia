print("hello")

import pathlib
import textwrap
import google.generativeai as genai
from secureKey import GEMENI_API_KEY

# “Give me the content for learning python , Make the list comprehensive return it as a json with major topic as the attribute and minor topics as lits value 
# example {“Level”:[{“Main topic”:[“minor topic1”,”minor topic2”]}]}. where level referes to begiiner, advanvce etc”
genai.configure(api_key=GEMENI_API_KEY)

def getGeminiModels():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
        
def generateText():
    # welcome back
    model = genai.GenerativeModel('gemini-1.5-flash')
    # model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(
        '''Give me the topics for learning driving car ,
          return them as a  json with major topic as the attribute and minor topics as list value
            example 
            {"Level":
            [
                {"Main Topic 1":["minor topic1","minor topic2"]}]}.
                 
                where level referes to beginer, advance etc 
                and topic referes to the subject matter topic
        
        The return should be json and only json '''
                  )
    
    print(response.text)
  
    # print(response.prompt_feedback)

if __name__ == "__main__":
   generateText()
  