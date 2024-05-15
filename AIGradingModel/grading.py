from myapp.models import Exam, ExamSubmission, ExamSubmissionOCR
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(student_answer, model_answer):
    student_embedding = sbert_model.encode(student_answer)
    model_embedding = sbert_model.encode(model_answer)
    similarity_score = cosine_similarity([student_embedding], [model_embedding])[0][0]
    similarity_score = similarity_score * 8  # Max score for similarity is 8
    return similarity_score

def calculate_keyword_score(student_answer, keywords):
    if not keywords:  # If no keywords provided
        return 2  # Max score for keywords is 2
    keyword_list = [keyword.strip() for keyword in keywords.split(',')]
    total_keywords = len(keyword_list)
    keyword_score = sum(keyword in student_answer for keyword in keyword_list)
    return (keyword_score / total_keywords) * 2  # Max score for keywords is 2

def StartGrading(exam_id):
    exam_submissions = ExamSubmission.objects.filter(exam_id=exam_id)

    for submission in exam_submissions:
        # Get the exam model answer and keywords
        model_answer = submission.exam.model_answer
        keywords = submission.exam.keywordsList

        # Calculate semantic similarity and keyword score
        semantic_similarity = calculate_similarity(submission.student_answer, model_answer)
        keyword_score = calculate_keyword_score(submission.student_answer, keywords)

        # Calculate question grade
        submission.score = semantic_similarity + keyword_score
        submission.is_graded = True
        # Update the submission
        submission.save()

    return exam_submissions


def StartGradingOCR(exam_id):
    exam_submissions = ExamSubmissionOCR.objects.filter(exam_id=exam_id)

    for submission in exam_submissions:
        # Get the exam model answer and keywords
        model_answer = submission.exam.model_answer
        keywords = submission.exam.keywordsList

        # Calculate semantic similarity and keyword score
        semantic_similarity = calculate_similarity(submission.extracted_text, model_answer)
        keyword_score = calculate_keyword_score(submission.extracted_text, keywords)

        # Calculate question grade
        submission.score = semantic_similarity + keyword_score
        submission.is_graded = True
        # Update the submission
        submission.save()

    return exam_submissions

