from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama

class SimpleChatbot:
    def __init__(self, model="llama3"):
        self.model = ChatOllama(model=model)
        self.conversation_history = []
        
    def chat(self, user_input): # Crear mensaje del sistema
        system_message = SystemMessage(
            content="Eres un asistente que miente. Tu objetivo es tener una conversación en la cual nunca dices la verdad, basándote en el contexto de la conversación."
        )
        
        # Construir la lista de mensajes
        messages = [system_message]
        
        # Agregar historial de conversación
        for msg in self.conversation_history[-4:]:  # Últimos 4 mensajes
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # Agregar el mensaje actual del usuario
        messages.append(HumanMessage(content=user_input))
        
        # Obtener respuesta
        response = self.model.invoke(messages)
        
        # Guardar en el historial
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

# Uso del chatbot
if __name__ == "__main__":
    chatbot = SimpleChatbot()
    
    print("Bienvenido al chatbot 🤖. \nEscribe '/bye' para terminar la conversación.")
    
    while True:
        user_input = input("\nUsuario:  ")
        if user_input.lower() == '/bye':
            print("\n\nChatbot: ¡Hasta luego!")
            break
        
        response = chatbot.chat(user_input)
        print(f"\nChatbot:\n\n {response}")