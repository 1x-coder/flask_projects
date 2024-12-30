import os
import openai

from flask import Flask, render_template, request

openai.api_key = os.getenv("OPENAI_API_KEY")

with open('prompt_history.txt', 'r') as file:
    prompt_history = file.read()

def get_response(prompt_history, new_topic):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt_history + "topic: " + new_topic + "\nhaiku: ",
    temperature=0.8,
    max_tokens=498,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["##"]
  )
  return(response["choices"][0]["text"])
  

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    # Process user_message using your chatbot logic
    # Generate a response
    return render_template('index.html', message=user_message, response=get_response(prompt_history, user_message))

@app.route('/')
def home():
    return render_template('index.html', response='')

if __name__ == '__main__':
    app.run(debug=True)
