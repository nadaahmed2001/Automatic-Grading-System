import veryfi
from veryfi import Client

def OCR_Verify_Model(file):
    client_id = 'vrfBSSdeL2mSPlLYXot3dVM6YI8DLABMuFMS7Hb'
    client_secret = ''
    username = '11410120201210'
    api_key = ''
    # api_key = ''

    categories = ['Grocery', 'Utilities', 'Travel']
    file_path = file
    veryfi_client = Client(client_id, client_secret, username, api_key)
    response = veryfi_client.process_document(file_path, categories=categories)
    # Accessing and printing the ocr_text with corrected spacing
    ocr_text = response['ocr_text']
    lines = ocr_text.split('\n')
    student_id = ""
    student_name = ""
    student_answer = ""

    for i, line in enumerate(lines):
        stripped_line = line.replace(' ', '').strip()
        if 'ID' in line:
            # Check if ID is on the same line
            id_line = line.replace('ID', '').strip()
            student_id = id_line
            # Check if ID is on the previous line
            if i > 0:
                prev_line = lines[i - 1].replace(' ', '').strip()
                if prev_line.isdigit():
                    student_id = lines[i - 1].strip()
        if 'Name' in line:
            student_name = line.split('Name', 1)[1].strip()
        if 'Answer' in line:
            student_answer = line.split('Answer', 1)[1].strip()
            continue
        student_answer += " " +line.strip() + "\n"

    return student_id.replace(' ',''), student_name, student_answer