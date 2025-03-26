import openai
import os
import fitz

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RUTA_DOCUMENTO = os.path.join(os.getcwd(), "actual IPS.pdf")

class Sueroterapia:
    def __init__(self, contenido):
        self.contenido = contenido
        self.subagentes = {
            "¿Qué es la sueroterapia y sus beneficios?": Subagente("¿Qué es la sueroterapia y sus beneficios?", contenido, "high"),
            "Détox Básico": Subagente("Détox Básico", contenido, "medium"),
            "Détox Avanzado": Subagente("Détox Avanzado", contenido, "medium"),
            "Metabólico": Subagente("Metabólico", contenido, "medium"),
            "Metodos de Pago": Subagente("Metodos de Pago", contenido, "low"),
            
        }
    
    def seleccionar_subagente(self, prompt):
        prompt_lower = prompt.lower()
        for clave, subagente in self.subagentes.items():
            if clave.lower() in prompt_lower:
                return subagente
        if any(word in prompt_lower for word in ["precio", "cuesta"]):
            return self.subagentes["Détox Básico"]  
        if any(word in prompt_lower for word in ["pago", "método de pago", "cómo pagar"]):
            return self.subagentes["Métodos de Pago"]  
        return self.subagentes["¿Qué es la sueroterapia y sus beneficios?"]  
    
    def responder(self, prompt):
        subagente = self.seleccionar_subagente(prompt)
        return subagente.generar_respuesta(prompt)

class Subagente:
    def __init__(self, nombre, contenido, nivel):
        self.nombre = nombre
        self.contenido = contenido
        self.nivel = nivel
    
    def generar_respuesta(self, prompt):
        try:
            niveles_config = {
                "low": {"temperature": 0.2, "max_tokens": 200, "top_p": 0.5},
                "medium": {"temperature": 0.7, "max_tokens": 500, "top_p": 0.8},
                "high": {"temperature": 1.0, "max_tokens": 1000, "top_p": 1.0}
            }
            
            config = niveles_config[self.nivel]
            
            prompt_completo = f"Explica detalladamente sobre '{self.nombre}' en relación a la siguiente pregunta: '{prompt}'.\n\n{self.contenido}"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=config['temperature'],
                max_tokens=config['max_tokens'],
                top_p=config['top_p'],
                frequency_penalty=0,
                presence_penalty=0,
            )
            
            return f"Subagente: {self.nombre}\n{response.choices[0].message.content}"
        except Exception as e:
            return f"Error al procesar la pregunta con {self.nombre}: {str(e)}"

def leer_documento(ruta_archivo):
    try:
        with fitz.open(ruta_archivo) as doc:
            contenido = ""
            for pagina in doc:
                contenido += pagina.get_text("text") + "\n"
            return contenido if contenido.strip() else "El documento está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

contenido = leer_documento(RUTA_DOCUMENTO)

if contenido.startswith("Error"):
    print(contenido)
else:
    sueroterapia_agente = Sueroterapia(contenido)
    prompt_usuario = input("Ingrese su pregunta: ")
    respuesta = sueroterapia_agente.responder(prompt_usuario)
    print(respuesta)
