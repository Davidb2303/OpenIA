import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Variable de entorno de mi windows

respuesta = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "¿Para que estudio?"}]
)

print(respuesta.choices[0].message.content)
