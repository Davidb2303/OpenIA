import openai
import os
import fitz

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RUTA_DOCUMENTO = os.path.join(os.getcwd() ,"actual IPS.pdf")

print(f"📂 Buscando el archivo en: {RUTA_DOCUMENTO}")

def leer_documento(ruta_archivo):
    
    try:
        with fitz.open(ruta_archivo) as doc:
            contenido = ""
            for pagina in doc:
                contenido += pagina.get_text("text")+"\n"

            return contenido if contenido.strip() else "El documento está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

def analizar_documento(contenido, nivel='high'):
    
    
    
    try:
        niveles_config = {
            "low": {"temperature": 0.2, "max_tokens": 100, "top_p": 0.5},
            "medium": {"temperature": 0.7, "max_tokens": 256, "top_p": 0.8},
            "high": {"temperature": 1.0, "max_tokens": 400, "top_p": 1.0}
        }
        
        config = niveles_config[nivel]

        prompt = f"Explica el tratamiento de sueroterapia con un nivel de razonamiento {nivel}.\n\n{contenido}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=config['temperature'],
            max_tokens=config['max_tokens'],
            top_p=config['top_p'],
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al procesar el documento: {str(e)}"

contenido = leer_documento(RUTA_DOCUMENTO)

if contenido.startswith("Error"):
    print(contenido)
else:
    resultado = analizar_documento(contenido)
    print("Resumen del documento:")
    print(resultado)