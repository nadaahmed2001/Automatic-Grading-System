import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY = 'AIzaSyCub9APQCFZ0wP3ggQ0qMq96dS2cVB3CuM'
# GOOGLE_API_KEY ='' #To test error handling
genai.configure(api_key=GOOGLE_API_KEY)

def OCR_Gemini_Model(file, edit):

    file = PIL.Image.open(file)

    model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")
    model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

    if edit == 'true':
        student_answer = model_1.generate_content(["extract text that is written in the area of 'Answer:' and correct words that are written incorrectly,without description", file])
    else:
        student_answer = model_2.generate_content(["extract text that is written in the area of 'Answer:' and don't correct words that are written incorrectly , give me the extracted text only,without description", file])

    student_id = model_1.generate_content(["write only numbers was written in the area of word 'ID:' without description", file])
    student_name= model_1.generate_content(["write only text was written in the area of word 'Name:' without description", file])


    return student_id.text.replace(' ',''), student_name.text, student_answer.text
