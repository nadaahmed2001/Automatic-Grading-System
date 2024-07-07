import google.generativeai as genai
import PIL.Image
import io
from pathlib import Path
from pypdf import PdfReader
import PIL.Image
import io
import re


GOOGLE_API_KEY = ''
genai.configure(api_key=GOOGLE_API_KEY)

# !pip install pypdf

def check_file_extension(file_path):
    file_extension = Path(file_path).suffix.lower()
    if file_extension == '.pdf':
        return "PDF"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return "image"
    else:
        return "Unknown file type."

def OCR_Gemini_Model(file,edit='false'):
  
  model_1 = genai.GenerativeModel(model_name="gemini-pro-vision")
  model_2 = genai.GenerativeModel(model_name="gemini-1.5-flash")

  if(check_file_extension(file)=="PDF"):
        reader = PdfReader(file)
        page = reader.pages[0]
        image_bytes = page.images[0].data 

        image = PIL.Image.open(io.BytesIO(image_bytes))

        file = image 
  else:
      file = PIL.Image.open(file)  # Pass the file path, not the image object

  if(edit=='true'):
    # Pass the image object to the model, not the file path
    answer_text = model_1.generate_content(["write only text was written in the area of word ""Answer"",and edit words written incorectly ",file])
  else:
    answer_text = model_2.generate_content(["write only text was written in the area of word ""Answer"", and do not edit any word", file]) 

  student_id   = model_2.generate_content(["write only numbers was written in the area of word ""ID"" without description", file]) 
  student_name = model_2.generate_content(["write only text was written in the area of word ""Name"" without description", file]) 


  return student_id.text, student_name.text, answer_text.text
