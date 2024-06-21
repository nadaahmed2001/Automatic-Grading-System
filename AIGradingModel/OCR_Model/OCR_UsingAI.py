import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY='AIzaSyAtW0576BvHlrWHvAVguRRYzp_Afm9z7uc'
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_and_ID(file,edit='false'):

  file = PIL.Image.open(file)

  model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")
  model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

  if(edit=='true'):
    answer_text = model_1.generate_content(file)
  else:
    answer_text = model_2.generate_content(["write text was written in the photo as it without the first line containing only numbers,and don't edit any word", file])

  student_id  = model_1.generate_content(["write what was written in the first line containing numbers in the photo", file])
  
  return student_id.text,answer_text.text
