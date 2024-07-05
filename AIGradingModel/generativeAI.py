from groq import Groq


api_key = ''

client = Groq(api_key=api_key)
def generate_model_answer(question, constraints):
    try:
        model = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Explain {question}, {constraints}",
                }
            ],
            model="llama3-8b-8192",
        )
        print(model.choices[0].message.content)
        return model.choices[0].message.content

    except Exception as e:
        print(f"Error generating content: {e}")
        return None
    
