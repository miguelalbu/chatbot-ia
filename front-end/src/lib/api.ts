const API_URL = "http://localhost:8000/api"; 

export const chatService = {
  // Envia a mensagem e o ID da sessão
  sendMessage: async (message: string, sessionId: string) => {
    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, session_id: sessionId }),
      });

      if (!response.ok) {
        throw new Error(`Erro API: ${response.status}`);
      }

      return await response.json(); // Retorna { response: "texto...", source: "..." }
    } catch (error) {
      console.error("Erro na requisição:", error);
      throw error;
    }
  },

  // Limpa o histórico no Redis ( Cache de memória da conversação )
  clearHistory: async (sessionId: string) => {
    const response = await fetch(`${API_URL}/chat/history/${sessionId}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Erro ao limpar histórico");
    return await response.json();
  }
};