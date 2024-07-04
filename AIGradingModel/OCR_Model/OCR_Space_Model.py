import requests
import json
import os


def ocr_space_file(file, overlay=False, api_key='1b70baf52f88957', language='eng'):
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

        extracted_text = ocr_space_file(file=file)

        response_data = json.loads(extracted_text)
    
        extracted_text_concatenated = response_data["ParsedResults"][0]["ParsedText"] if "ParsedResults" in response_data else ""

        lines = extracted_text_concatenated.split('\n')
        
        student_ID = lines[0].replace('ID', '').replace('1D','').replace(' ', '').replace('\n', '')
        student_Name = lines[1].replace('Name', '')
    
        student_answer = lines[2:]
        student_answer = [answer.strip() for answer in student_answer if answer.strip()]
        student_answer = '\n'.join(student_answer)

        return student_ID, student_Name, student_answer
