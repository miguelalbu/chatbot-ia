import { cn } from "@/lib/utils";

export interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.sender === "user";

  return (
    <div
      className={cn(
        "flex w-full mb-4 animate-in fade-in-0 slide-in-from-bottom-2 duration-300",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[75%] md:max-w-[60%] rounded-2xl px-4 py-3 shadow-sm",
          isUser
            ? "bg-chat-user text-chat-user-foreground rounded-br-md"
            : "bg-chat-bot text-chat-bot-foreground rounded-bl-md border border-border"
        )}
      >
        <p className="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
          {message.text}
        </p>
        <span className={cn(
          "text-[11px] mt-1 block opacity-60",
          isUser ? "text-right" : "text-left"
        )}>
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </span>
      </div>
    </div>
  );
};
