from flask import Flask, render_template, request, session

import openai
import secrets
import certifi
import pip_system_certs.wrapt_requests

# need to install: pip install openai==0.28
# pip install certifi

# Flask Setup
app = Flask(__name__)
app.secret_key = secrets.token_hex(24)  # Set a secret key for Flask session

# OpenAI Setup (You can place this part in a separate configuration file)
openai.api_type = "azure"
openai.api_base = "https://openai-api.mckesson.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "4116ac52c8ea419c885764ae2b2c990b"
openai.api_cert = certifi.where() 

def get_gpt(conversation, user_input):
    try:
        # Add user input to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Call OpenAI API for text completion
        response = openai.ChatCompletion.create(
            engine="mt-azureopenai-ref-35turbo",
            messages=conversation,
            temperature=0.05,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        # Get GPT-3 response
        gpt_response = response.choices[0]['message']['content']

        # Add GPT response to the conversation
        conversation.append({"role": "assistant", "content": gpt_response})

        return gpt_response, conversation
    except Exception as e:
        print("Error during text generation:", e)
        raise

def get_last_5_items(conversation):
    return conversation[-5:]


@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    if request.method == 'GET':
        print("GET request received")
        last_5_items = get_last_5_items(session.get('conversation', []))
        return render_template('index.html', generated_text=None)
    
    elif request.method == 'POST':
        try:
            print("POST request received")
            user_input = request.form.get('prompt', '')

            # Retrieve the chat session or initialize an empty conversation
            conversation = session.get('conversation', [])

            # Get GPT response
            gpt_response, updated_conversation = get_gpt(conversation, user_input)
            session['conversation'] = updated_conversation

            return render_template('index.html', generated_text=gpt_response, error=None)
        except Exception as e:
            print("Error during text generation:", e)
            error_message = f"Error: {str(e)}"
            return render_template('index.html', generated_text=None, error=error_message), 500
    else:
        return "Unsupported HTTP method"

if __name__ == '__main__':
    app.run(debug=False)
