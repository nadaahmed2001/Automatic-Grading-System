import requests
import json
import os


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
    extracted_text_json = ocr_space_file(file)
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