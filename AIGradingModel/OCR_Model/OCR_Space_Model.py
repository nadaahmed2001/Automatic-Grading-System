import requests
import json
import os
from pathlib import Path
from pypdf import PdfReader
import PIL.Image
import io
import re

def check_file_extension(file_path):
    file_extension = Path(file_path).suffix.lower()
    if file_extension == '.pdf':
        return "PDF"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return "image"
    else:
        return "Unknown file type."

def ocr_space_file(file, overlay=False, api_key='', language='eng'):
# def ocr_space_file(file, overlay=False, api_key='', language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'detectOrientation': 'true',
               'scale' : 'true',
               'OCREngine': 2,
              }
    with open(file, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={file: f},
                          data=payload,
                          )
    return r.content.decode()

def OCR_Space_Model(file):
    if(check_file_extension(file)=="PDF"):
        reader = PdfReader(file)
        page = reader.pages[0]
        image_bytes = page.images[0].data 

        image = PIL.Image.open(io.BytesIO(image_bytes))

        temp_image_path = "temp_image.jpg" 
        image.save(temp_image_path)
        file_path = temp_image_path 
    else:
        file_path = file

    extracted_text_json = ocr_space_file(file_path)
    response_data = json.loads(extracted_text_json)
    
    text = response_data["ParsedResults"][0]["ParsedText"] if "ParsedResults" in response_data else ""

    lines = text.strip().split('\n')
    if lines:
        student_id = lines[0].replace('ID', '').replace('1D','').replace('D','').replace(' ', '').replace('\n', '')
        student_name = lines[1].replace('Name', '')
        
        answer_text = '\n'.join(lines[2:])
        answer_text = answer_text.replace('Answer','').replace('Answor', '')
    else:
        student_id, student_name, answer_text = '', ''

    return student_id, student_name ,answer_text
