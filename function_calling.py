import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_weather(city):
    url =f"https://api.open-meteo.com/v1/forecast?latitude=40.4168&longitude=-3.7038&current=temperature_2m,weathercode"
    response = requests.get(url)
    data = response.json()
    temp = data["current"]["temperature_2m"]
    return json.dumps({"city": city, "temperature": temp, "unit": "celcius"})

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                }
            },
            "required": ["city"]
        }
    }
]

messages = [
    {"role": "system", "content": "You are a helpful weather assistant."},
    {"role": "user", "content": "What's the weather like in Madrid"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    weather_result = get_weather(arguments["city"])
    
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": weather_result
    })

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print(final_response.choices[0].message.content)