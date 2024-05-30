import openpyxl
from django.http import HttpResponse
from myapp.models import ExamSubmissionOCR

def export_ocr_grades_to_excel(exam_id):
    # Get all the OCR submissions for the exam
    submissions = ExamSubmissionOCR.objects.filter(exam_id=exam_id).values('student_id', 'score')

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['ID', 'Grade'])
    for submission in submissions:
        sheet.append([submission['student_id'], submission['score']])

    # the MIME type for Microsoft Excel Open XML Spreadsheet (XLSX) .
    # This ensures that the browser recognizes the response as an Excel file and handles it accordingly (e.g., by prompting the user to download it).
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{exam_id}_ocr_grades.xlsx"'
    workbook.save(response)
    
    return response
