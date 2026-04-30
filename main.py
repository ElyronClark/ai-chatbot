import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation = [
    {"role": "system", "content": """You are a customer support agent for Techflow,
     a project management Saas. You are helpful, professional, and concise."""}
]

print("TechFlow Support Chat (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break

    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        stream=True
    )

    print(f"TechFlow: ", end="", flush=True)
    assistant_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            assistant_message += text
    print("\n")

    conversation.append({"role": "assistant", "content": assistant_message})