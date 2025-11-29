import { useState, useEffect } from "react";
import { chatService } from "../lib/api";
import { Message } from "@/components/ChatMessage";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      text: "Olá! Sou o assistente da Luar Cosméticos. Como posso ajudar com perfumes hoje?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");

  // 1. Gera ID de Sessão Único ao abrir o site (Persistente)
  useEffect(() => {
    let storedId = localStorage.getItem("chat_session_id");
    if (!storedId) {
      storedId = "user_" + Math.random().toString(36).substring(2, 9);
      localStorage.setItem("chat_session_id", storedId);
    }
    setSessionId(storedId);
  }, []);

  // 2. Função de Enviar Mensagem
  const sendMessage = async (text: string) => {
    if (!text.trim() || !sessionId) return;

    // Adiciona msg do usuário na tela
    const userMsg: Message = {
      id: Date.now().toString(),
      text: text,
      sender: "user",
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Chama o Backend
      const data = await chatService.sendMessage(text, sessionId);
      
      // Adiciona resposta do Bot
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response, // O texto que vem do Gemini
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      const errorMsg: Message = {
        id: Date.now().toString(),
        text: "Desculpe, estou com problemas de conexão com o servidor. 😓",
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  // 3. Função de Limpar Conversa
  const clearChat = async () => {
    if (!sessionId) return;
    try {
      await chatService.clearHistory(sessionId);
      setMessages([{
        id: Date.now().toString(),
        text: "Histórico limpo! Podemos começar um novo assunto.",
        sender: "bot",
        timestamp: new Date(),
      }]);
    } catch (error) {
      console.error("Erro ao limpar", error);
    }
  };

  return { messages, sendMessage, clearChat, isLoading };
}