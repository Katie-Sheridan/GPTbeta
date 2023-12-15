import openai

# OpenAI Setup (You can place this part in a separate configuration file)
openai.api_type = "azure"
openai.api_base = "https://openai-api.mckesson.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "4116ac52c8ea419c885764ae2b2c990b"

# Set Google Cloud credentials file path
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\epkkvnf\\OneDrive - McKesson Corporation\\Documents\\gcp_dev_serv_acct_key.txt"

conversation = []

# Define the prompt
initial_prompt = "I am an AI assistant. I'm here to help you with information. Feel free to ask me any question or make a request."

print("AI Assistant:", initial_prompt)


while True:
    user_input = input("User: ")
    
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

    # Display GPT response
    print(f"Assistant: {gpt_response}")
    
