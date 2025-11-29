import { useState, useRef, useEffect } from "react";
import { ChatMessage, Message } from "@/components/ChatMessage";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Olá! Como posso ajudar você hoje?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Mock function para simular envio de mensagem
  const sendMessage = async (text: string): Promise<string> => {
    // Aqui será integrado com o backend futuramente
    return new Promise((resolve) => {
      setTimeout(() => {
        const responses = [
          "Entendi! Como posso ajudar com isso?",
          "Interessante! Conte-me mais.",
          "Claro, posso te ajudar com isso.",
          "Ótima pergunta! Vou pensar sobre isso.",
        ];
        resolve(responses[Math.floor(Math.random() * responses.length)]);
      }, 500);
    });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    // Simula resposta do bot
    const botResponse = await sendMessage(inputValue);
    const botMessage: Message = {
      id: (Date.now() + 1).toString(),
      text: botResponse,
      sender: "bot",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, botMessage]);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-4 shadow-sm">
        <h1 className="text-xl font-semibold text-foreground">Chat</h1>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-4 py-6 md:px-8">
        <div className="mx-auto max-w-3xl">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="border-t border-border bg-card px-4 py-4 md:px-8 shadow-lg">
        <div className="mx-auto max-w-3xl flex gap-3">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite sua mensagem..."
            className="flex-1 bg-input border-border focus-visible:ring-accent transition-all"
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim()}
            className="bg-accent text-accent-foreground hover:bg-accent/90 transition-all shadow-sm"
            size="icon"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </footer>
    </div>
  );
};

export default Index;
