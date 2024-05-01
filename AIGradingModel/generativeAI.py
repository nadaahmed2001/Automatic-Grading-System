import textwrap
from IPython.display import display, Markdown

import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util

GOOGLE_API_KEY = 'AIzaSyCJH_fwy1ryrGkA30qHwkcGL6XFUUQhHo4'
genai.configure(api_key=GOOGLE_API_KEY)

def generate_model_answer(question):
    # Initialize the generative model
    model = genai.GenerativeModel('gemini-pro')

    # Generate the model response
    model_prompt = f"Explain {question}"+ "In short answer"
    model_response = model.generate_content(model_prompt).text

    return model_response
