import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY='AIzaSyAtW0576BvHlrWHvAVguRRYzp_Afm9z7uc'
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_and_ID(file):

  #open the file
  file = PIL.Image.open(file)

  #this model to extract and edit the words were written incorrectly.
  model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")

  #this model writes the words extracted as it without editting on them.
  model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

  student_id  = model_1.generate_content(["write what was written in the first line containing numbers in the photo", file])
  answer_text = model_2.generate_content(["write text was written in the photo as it without the first line containing only numbers", file])

  return student_id, answer_text
