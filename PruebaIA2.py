import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Variable de entorno de mi windows

respuesta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Dame las mejores universidades de Bogotá y en que puesto está la universitaria de Colombia"}],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    #stop=["\n"],
    n=5,
    reasoning="low"
)

print(respuesta.choices[0].message.content)
