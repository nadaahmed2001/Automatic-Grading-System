from myapp.models import Exam, ExamSubmission, ExamSubmissionOCR
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(student_answer, model_answer):
    student_embedding = sbert_model.encode(student_answer)
    model_embedding = sbert_model.encode(model_answer)
    similarity_score = cosine_similarity([student_embedding], [model_embedding])[0][0]
    # similarity_score = similarity_score
    return similarity_score

def calculate_keyword_score(student_answer, keywords):
    keyword_list = [keyword.strip() for keyword in keywords.split(',')]
    total_keywords = len(keyword_list)
    keyword_score = sum(keyword in student_answer for keyword in keyword_list)
    return (keyword_score / total_keywords)


def GradeWithKeywords(student_answer, model_answer, keywords):
    similarity_score = calculate_similarity(student_answer, model_answer)
    keyword_score = calculate_keyword_score(student_answer, keywords)
    question_grade = (similarity_score*8 +keyword_score*2)
    print("From function GradeWithKeywords, Question Grade: ", question_grade)
    return question_grade

def GradewithNoKeywords(student_answer, model_answer):
    # Calculate semantic similarity
    semantic_similarity = calculate_similarity(student_answer, model_answer)
    # Calculate question grade
    question_grade = semantic_similarity * 10
    print("from function GradeWithNoKeywords, Question Grade: ", question_grade)
    return question_grade


def StartGrading(exam_id):
    exam_submissions = ExamSubmission.objects.filter(exam_id=exam_id)

    for submission in exam_submissions:
        # Get the exam model answer and keywords
        model_answer = submission.exam.model_answer
        keywords = submission.exam.keywordsList

        if keywords == "":
            submission.score = GradewithNoKeywords(submission.student_answer, model_answer)
        else:
            submission.score = GradeWithKeywords(submission.student_answer, model_answer, keywords) 

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

        if keywords == "":
            # Calculate semantic similarity and keyword score
            submission.score = GradewithNoKeywords(submission.extracted_text, model_answer)
        else:
            submission.score = GradeWithKeywords(submission.extracted_text, model_answer, keywords)

        submission.is_graded = True
        # Update the submission
        submission.save()

    return exam_submissions

