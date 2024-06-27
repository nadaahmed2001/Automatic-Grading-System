import google.generativeai as genai
import PIL.Image
# import os

GOOGLE_API_KEY = 'AIzaSyBESXyRjSDiJTWA9IxeG5bZveutG-j5Y3c'
genai.configure(api_key=GOOGLE_API_KEY)
# genai.configure(api_key=os.environ['AIzaSyBESXyRjSDiJTWA9IxeG5bZveutG-j5Y3c'])


def extract_text_and_ID(file, edit='false'):
    file = PIL.Image.open(file)
    print("File: ", file)

    model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")
    model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

    if edit == 'true':
        print("I've entered the condition edit = true")
        student_answer = model_1.generate_content(["extract text that is written in the area of 'Answer:' and correct words that are written incorrectly, give me the extracted text only, don't add anything else", file])
        print("Student answer from model 1: ", student_answer.text)
    else:
        print("I've entered the condition edit = false")
        student_answer = model_2.generate_content(["extract text that is written in the area of 'Answer:' and don't correct words that are written incorrectly , give me the extracted text only, don't add anything else", file])
        print("Student answer from model 2: ", student_answer.text)

    student_id = model_1.generate_content(["write only numbers was written in the boxes of word 'ID:' without description", file])
    student_name = model_1.generate_content(["write only text was written in the box of word 'Name:'", file])

    print("Student ID: ", student_id.text)
    print("Student Name: ", student_name.text)

    return student_id.text, student_name.text, student_answer.text
