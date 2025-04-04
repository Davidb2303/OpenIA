import openai
import os
import fitz  
import json

API_KEY = "" #Reemplazar por Api Key

RUTA_DOCUMENTO = os.path.join(os.getcwd(), "actual IPS.pdf")

class Sueroterapia:
    def __init__(self, contenido):
        self.contenido = contenido
        self.subagentes = {
            "¿Qué es la sueroterapia y sus beneficios?": Subagente("¿Qué es la sueroterapia y sus beneficios?", contenido, "informativo", "high"),
            "Détox Básico": Subagente("Détox Básico", contenido, "detalle-medio", "medium"),
            "Détox Avanzado": Subagente("Détox Avanzado", contenido, "detalle-alto", "high"),
            "Metabólico": Subagente("Metabólico", contenido, "detalle-medio", "medium"),
            "Métodos de Pago": Subagente("Métodos de Pago", contenido, "transaccional", "low")
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
        if any(word in prompt_lower for word in ["detox", "desintoxicación"]):
            return self.subagentes["Détox Básico"]
        return self.subagentes["¿Qué es la sueroterapia y sus beneficios?"]  
   
    def responder(self, prompt):
        subagente = self.seleccionar_subagente(prompt)
        return subagente.generar_respuesta(prompt)

class Subagente:
    def __init__(self, nombre, contenido, categoria, reasoning_effort):
        self.nombre = nombre
        self.contenido = contenido
        self.categoria = categoria
        self.reasoning_effort = reasoning_effort
   
    def generar_respuesta(self, prompt):
        try:
            client = openai.OpenAI(api_key=API_KEY)
            
            additional_params = {}
            if self.reasoning_effort == "high":
                
                additional_params["temperature"] = 0.3
            elif self.reasoning_effort == "medium":
                additional_params["temperature"] = 0.5
            elif self.reasoning_effort == "low":
                additional_params["temperature"] = 0.7
            
            
            system_message = f"""
            Eres un experto en '{self.nombre}'.
            Usa la siguiente información del documento para responder con precisión.
            
            INFORMACIÓN DEL DOCUMENTO:
            {self.contenido}
            
            Categoría: {self.categoria}
            """
            
            
            response = client.chat.completions.create(
                model="o3-mini",  
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                **({} if "o3-mini" in "o3-mini" else additional_params)
            )
            
            
            respuesta = response.choices[0].message.content
            
            return json.dumps({
                "subagente": self.nombre,
                "categoria": self.categoria,
                "reasoning_effort": self.reasoning_effort,
                "respuesta": respuesta
            }, indent=4, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "error": f"Error al procesar la pregunta con {self.nombre}: {str(e)}"
            }, indent=4, ensure_ascii=False)

def leer_documento(ruta_archivo):
    try:
        with fitz.open(ruta_archivo) as doc:
            contenido = "".join(pagina.get_text("text") + "\n" for pagina in doc)
            return contenido if contenido.strip() else "El documento está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

if __name__ == "__main__":
    print("Iniciando el agente de Sueroterapia...")
    contenido = leer_documento(RUTA_DOCUMENTO)
    if contenido.startswith("Error"):
        print(contenido)
    else:
        print("Documento cargado correctamente.")
        sueroterapia_agente = Sueroterapia(contenido)
        while True:
            try:
                prompt_usuario = input("\nIngrese su pregunta (o 'salir' para terminar): ")
                if prompt_usuario.lower() in ['salir', 'exit', 'q', 'quit']:
                    print("Gracias por usar el agente de Sueroterapia. ¡Hasta pronto!")
                    break
                
                print("Procesando su pregunta...")
                respuesta = sueroterapia_agente.responder(prompt_usuario)
                print("\nRESPUESTA:")
                print(respuesta)
            except KeyboardInterrupt:
                print("\nPrograma interrumpido. Saliendo...")
                break
            except Exception as e:
                print(f"\nError inesperado: {str(e)}")
