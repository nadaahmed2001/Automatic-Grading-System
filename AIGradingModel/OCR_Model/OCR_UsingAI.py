import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY = 'AIzaSyAtW0576BvHlrWHvAVguRRYzp_Afm9z7uc'
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_and_ID(file, edit='false'):   

  file = PIL.Image.open(file)

  model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")
  model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

  if(edit=='true'):
    student_answer = model_1.generate_content(["write text that was written in the area of word ""Answer:"", edit words written incorectly ", file])
  else:
    student_answer = model_2.generate_content(["write text that was written in the area of word ""Answer:"", and do not edit any word", file])

  student_id   = model_1.generate_content(["write only numbers was written in the boxes of word ""ID:"" without description", file])
  student_name = model_1.generate_content(["write only text was written in the box of word ""Name:"" ",file])

  return student_id.text, student_name.text, student_answer.text
