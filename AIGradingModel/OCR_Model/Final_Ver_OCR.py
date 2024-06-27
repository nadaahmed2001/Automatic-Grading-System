from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from google.colab.patches import cv2_imshow # Import cv2_imshow for Colab
from PIL import Image
import requests
import cv2
import numpy as np
import os
import json

def Segment_exam_Paper(file):
    # Constants
    KNOWN_LINE_DISTANCE_CM = 0.5  # Known distance between lines in cm
    PIXELS_PER_CM = 96 / 2.54  

    # Read the image
    img = cv2.imread(file)
    if img is None:
        print("Error: Image not loaded correctly.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Apply morphological operations to close gaps in the text lines
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Calculate horizontal projection profile
    hist = cv2.reduce(morph, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32S).reshape(-1)

    # Determine the number of pixels corresponding to the known line distance
    line_distance_pixels = int(KNOWN_LINE_DISTANCE_CM * PIXELS_PER_CM)

    # Initialize boundaries
    uppers = []
    lowers = []
    in_text = False

    for i, value in enumerate(hist):
        if value > 0 and not in_text:
            uppers.append(i)
            in_text = True
        elif value == 0 and in_text:
            lowers.append(i)
            in_text = False

    # Refine boundaries based on known line distance
    refined_uppers = []
    refined_lowers = []

    for i in range(len(uppers)):
        if i == 0 or (uppers[i] - refined_uppers[-1] >= line_distance_pixels):
            refined_uppers.append(uppers[i])
            refined_lowers.append(lowers[i])

    # Draw boundaries on the original image for visualization
    visualization_img = img.copy()
    for upper in refined_uppers:
        cv2.line(visualization_img, (0, upper), (img.shape[1], upper), (0, 255, 0), 2)
    for lower in refined_lowers:
        cv2.line(visualization_img, (0, lower), (img.shape[1], lower), (255, 0, 0), 2)

    # Initialize a list to store lines
    lines = []

    # Extract lines based on refined upper and lower boundaries
    for upper, lower in zip(refined_uppers, refined_lowers):
        line_img = img[upper:lower, :]
        if line_img.size > 0:  # Check if the image is not empty
            lines.append(line_img)

    cv2.destroyAllWindows()
    return lines


def extract_student_answer(file):

    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    # Exclude the first two images from the list (ID,Name)
    answer = file[2:]

    student_answer=""

    for line in answer:

        line_img = Image.fromarray(line).convert("RGB")
        # Update the processor to use a single mean value for grayscale normalization
        #processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', image_mean=0.5, image_std=0.5) 


        pixel_values = processor(images=line_img, return_tensors="pt").pixel_values

        generated_ids = model.generate(pixel_values)
        extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        extracted_text = extracted_text.strip()
        extracted_text = extracted_text[1:]
      
        student_answer += "\n" + extracted_text  # Concatenate extracted text
        student_answer = student_answer.strip()

    return student_answer


def ocr_space_file(filename, overlay=False, api_key='1b70baf52f88957', language='eng'):

        payload = {'isOverlayRequired': overlay,
                  'apikey': api_key,
                  'language': language,
                  'detectOrientation': 'true',
                  'scale' : 'true',
                  'OCREngine': 2,
                  }
        # Save the image to a temporary file
        temp_filename = "temp_image.png"
        filename.save(temp_filename)

        with open(temp_filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={temp_filename: f},
                              data=payload,
                              )
        # Remove the temporary file
        os.remove(temp_filename)

        return r.content.decode()

def extract_ID_Name_Answer(file):
    images = Segment_exam_Paper(file)

    extracted_ID   = json.loads(ocr_space_file(filename = Image.fromarray(images[0]).convert("RGB"), language='eng'))
    extracted_Name = json.loads(ocr_space_file(filename = Image.fromarray(images[1]).convert("RGB"), language='eng'))

    student_ID    = extracted_ID["ParsedResults"][0]["ParsedText"]
    student_Name  = extracted_Name["ParsedResults"][0]["ParsedText"]
    student_answer= extract_student_answer(images)

    return student_ID, student_Name , student_answer
