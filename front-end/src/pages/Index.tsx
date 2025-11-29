import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Trash2, Loader2 } from "lucide-react"; 
import { useChat } from "@/hooks/useChat"; 

const Index = () => {
  const { messages, sendMessage, clearChat, isLoading } = useChat();
  
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return; 

    const text = inputValue;
    setInputValue(""); 
    
    await sendMessage(text); 
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header Atualizado */}
      <header className="border-b border-border bg-card px-6 py-4 shadow-sm flex justify-between items-center">
        <div>
          <h1 className="text-xl font-semibold text-foreground">Luar Cosméticos AI</h1>
          <p className="text-xs text-muted-foreground">Assistente Virtual</p>
        </div>
        
        <Button 
          variant="ghost" 
          onClick={clearChat}
          title="Nova Conversa / Limpar Memória"
          className="text-muted-foreground hover:text-destructive flex items-center gap-2"
        >
          <Trash2 className="h-5 w-5" />
          <span className="text-sm">Limpar Histórico</span>
        </Button>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-4 py-6 md:px-8 bg-slate-50/50">
        <div className="mx-auto max-w-3xl space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          
          {/* Loading Atualizado */}
          {isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground text-sm p-4 animate-pulse">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Luar Cosméticos está digitando...</span>
            </div>
          )}
          
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
            placeholder="Pergunte sobre perfumes, preços ou dicas..."
            className="flex-1 bg-input border-border focus-visible:ring-accent transition-all"
            disabled={isLoading}
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="bg-accent text-accent-foreground hover:bg-accent/90 transition-all shadow-sm"
            size="icon"
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </div>
      </footer>
    </div>
  );
};

export default Index;