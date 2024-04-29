#SBERT_Grading_Model.py

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(student_answer, model_answer, sbert_model):
    # Ensure both inputs are strings
    student_answer = str(student_answer)
    student_embedding = sbert_model.encode(student_answer)
    model_embedding = sbert_model.encode(model_answer)
    similarity_score = cosine_similarity([student_embedding], [model_embedding])[0][0]
    similarity_score *= 8
    return similarity_score

def calculate_keyword_score(student_answer, keywords):
    if pd.isna(keywords): # If no keywords provided
        return 3
    keyword_list = [keyword.strip() for keyword in keywords.split(',')]
    total_keywords = len(keyword_list)
    keyword_score = sum(keyword in student_answer for keyword in keyword_list)
    return (keyword_score / total_keywords) * 2 # Max score for keywords is 2

def calculate_final_grades(student_answers_df, exam_questions_df, sbert_model):
    final_grades_df = pd.DataFrame(columns=['Student ID', 'Final Grade'])

    for index, row in student_answers_df.iterrows():
        final_grade = 0

        student_answer = row['Extracted Text']

        model_answer_row = exam_questions_df[exam_questions_df['ExamNum'] == 1]
        if not model_answer_row.empty:
            model_answer = model_answer_row['Model Answer'].values[0]
            keywords = model_answer_row['Teacher Keywords'].values[0]

            semantic_similarity = calculate_similarity(student_answer, model_answer, sbert_model)
            keyword_score = calculate_keyword_score(student_answer, keywords)

            final_grade = semantic_similarity + keyword_score

            final_grades_df = pd.concat([final_grades_df, pd.DataFrame({'Student ID': [row['Student ID']], 'Final Grade': [final_grade]})], ignore_index=True)

    return final_grades_df

def main():
    file_path = "Final_SBERT_Dataset.xlsx"
    student_answers_df = pd.read_excel(file_path, sheet_name="StudentAnswerExtracted")
    exam_questions_df = pd.read_excel(file_path, sheet_name="ExamQuestions")

    sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

    num_questions = exam_questions_df['ExamNum'].nunique()
    print("Number of questions:", num_questions)

    final_grades_df = calculate_final_grades(student_answers_df, exam_questions_df, sbert_model)

    with pd.ExcelWriter('Final_Grades.xlsx') as writer:
        final_grades_df.to_excel(writer, sheet_name='FinalGrades', index=False)

    print(final_grades_df)

if __name__ == "__main__":
    main()
