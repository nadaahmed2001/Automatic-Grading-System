import veryfi
from veryfi import Client
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

def OCR_Verify_Model(file):
    client_id = 'vrf6ndisxpgBtTaPCAVHwnecpJUn4ci9oAyOse7'
    client_secret = ''
    username = 'hadeer.fcai'
    api_key = ''

    categories = ['Grocery', 'Utilities', 'Travel']

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

    veryfi_client = Client(client_id, client_secret, username, api_key)
    response = veryfi_client.process_document(file_path, categories=categories)

    ocr_text = response['ocr_text']
    
    # Replace multiple spaces with a single space
    ocr_text = re.sub(r'\s+', ' ', ocr_text)
    
    lines = ocr_text.split('\n')

    student_id = response.get('invoice_number','')
      
    answer_start = ocr_text.find('Answer')
    name_start = ocr_text.find('Name') + len('Name')

    student_name = ocr_text[name_start:answer_start].strip()
    student_answer = ocr_text[answer_start:].strip().replace('Answer','')

    return student_id, student_name, student_answer
