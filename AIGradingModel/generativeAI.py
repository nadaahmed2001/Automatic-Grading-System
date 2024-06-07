import textwrap
from IPython.display import display, Markdown
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util

GOOGLE_API_KEY = 'AIzaSyAtW0576BvHlrWHvAVguRRYzp_Afm9z7uc'
genai.configure(api_key=GOOGLE_API_KEY)

def generate_model_answer(question, constraints):
    try:
        model = genai.GenerativeModel('gemini-pro')

        model_prompt = f"Explain {question}"
        if constraints:
            model_prompt += f" ,{constraints}"

        # Generate the model answer
        model_response = model.generate_content(model_prompt).text
        return model_response

    except Exception as e:
        print(f"Error generating content: {e}")
        return None
