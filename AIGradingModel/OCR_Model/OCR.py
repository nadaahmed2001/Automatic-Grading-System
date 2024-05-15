# ocr.py
import requests
import json

def ocr_space_file(file, overlay=False, api_key='1b70baf52f88957', language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
        'detectOrientation': 'true',
        'scale' : 'true',
        'OCREngine': 2,
    }
    with file.open('rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={file.name: f},
                          data=payload)
    return r.content.decode()

def extract_text_and_split(file):
    extracted_text_json = ocr_space_file(file)
    print("Extracted text: ", extracted_text_json.strip())
    response_data = json.loads(extracted_text_json)
    text = response_data["ParsedResults"][0]["ParsedText"] if "ParsedResults" in response_data else ""

    lines = text.strip().split('\n')
    if lines:
        student_id = lines[0]
        answer_text = ' '.join(lines[1:])
    else:
        student_id, answer_text = '', ''

    return student_id, answer_text
