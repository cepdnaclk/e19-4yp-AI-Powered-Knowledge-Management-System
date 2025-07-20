import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { ThemeToggle } from "@/components/theme-toggle";
import { LogOut, Send, Loader2, Bot, User, Brain, Sparkles } from "lucide-react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { ChatSidebar, ChatSession } from "@/components/ChatSidebar";

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface ChatSessionData extends ChatSession {
  messages: Message[];
}

const Dashboard = () => {
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string>('1');
  const [chatSessions, setChatSessions] = useState<Record<string, ChatSessionData>>({
    '1': {
      id: '1',
      title: 'New Chat',
      lastMessage: '',
      timestamp: new Date(),
      messageCount: 0,
      messages: [{
        id: "welcome",
        content: "Hello! I'm your RAG AI assistant. I can help answer questions based on your knowledge base. What would you like to know?",
        sender: "ai",
        timestamp: new Date()
      }]
    }
  });
  const { toast } = useToast();

  const currentMessages = chatSessions[currentChatId]?.messages || [];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: question,
      sender: 'user',
      timestamp: new Date(),
    };

    // Update current chat session with user message
    setChatSessions(prev => {
      const currentSession = prev[currentChatId];
      const updatedMessages = [...currentSession.messages, userMessage];
      
      return {
        ...prev,
        [currentChatId]: {
          ...currentSession,
          messages: updatedMessages,
          lastMessage: question,
          timestamp: new Date(),
          messageCount: updatedMessages.length,
          title: currentSession.title === 'New Chat' ? question.slice(0, 30) : currentSession.title
        }
      };
    });

    const currentQuestion = question;
    setQuestion('');
    setIsLoading(true);

    try {
      // Make API call to Flask RAG backend
      const response = await fetch('http://localhost:5000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: "dev-42",
          query: currentQuestion
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Check if the request was successful
      if (!data.success) {
        throw new Error('API request was not successful');
      }
      
      // Format the response with sources
      let aiResponseContent = data.response || 'Sorry, I couldn\'t generate a response.';
      
      // Add sources if available
      if (data.sources && data.sources.length > 0) {
        aiResponseContent += '\n\n**Sources:**';
        data.sources.forEach((source, index) => {
          aiResponseContent += `\n${index + 1}. ${source}`;
        });
      }
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponseContent,
        sender: 'ai',
        timestamp: new Date(),
      };

      // Update chat session with AI response
      setChatSessions(prev => {
        const currentSession = prev[currentChatId];
        const updatedMessages = [...currentSession.messages, aiMessage];
        
        return {
          ...prev,
          [currentChatId]: {
            ...currentSession,
            messages: updatedMessages,
            messageCount: updatedMessages.length,
            timestamp: new Date()
          }
        };
      });

    } catch (error) {
      console.error('API Error:', error);
      
      // Add error message to chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I encountered an error while processing your request: ${error instanceof Error ? error.message : 'Unknown error'}. Please make sure the Flask server is running on http://localhost:5000.`,
        sender: 'ai',
        timestamp: new Date(),
      };

      setChatSessions(prev => {
        const currentSession = prev[currentChatId];
        const updatedMessages = [...currentSession.messages, errorMessage];
        
        return {
          ...prev,
          [currentChatId]: {
            ...currentSession,
            messages: updatedMessages,
            messageCount: updatedMessages.length,
            timestamp: new Date()
          }
        };
      });

      toast({
        variant: "destructive",
        title: "Connection Error",
        description: "Failed to connect to the RAG API. Please ensure the Flask server is running.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChatSelect = (chatId: string) => {
    setCurrentChatId(chatId);
  };

  const handleNewChat = () => {
    const newChatId = Date.now().toString();
    const newChat: ChatSessionData = {
      id: newChatId,
      title: 'New Chat',
      lastMessage: '',
      timestamp: new Date(),
      messageCount: 0,
      messages: [{
        id: "welcome-" + newChatId,
        content: "Hello! I'm your RAG AI assistant. I can help answer questions based on your knowledge base. What would you like to know?",
        sender: "ai",
        timestamp: new Date()
      }]
    };
    
    setChatSessions(prev => ({
      ...prev,
      [newChatId]: newChat
    }));
    setCurrentChatId(newChatId);
  };

  const handleDeleteChat = (chatId: string) => {
    // TODO: Add confirmation dialog
    setChatSessions(prev => {
      const updated = { ...prev };
      delete updated[chatId];
      return updated;
    });
    
    // Switch to another chat if current one is deleted
    if (chatId === currentChatId) {
      const remainingChats = Object.keys(chatSessions).filter(id => id !== chatId);
      if (remainingChats.length > 0) {
        setCurrentChatId(remainingChats[0]);
      } else {
        handleNewChat();
      }
    }
  };

  const handleLogout = () => {
    // TODO: Implement actual logout logic
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    });
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gradient-bg">
        <ChatSidebar
          currentChatId={currentChatId}
          onChatSelect={handleChatSelect}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
        />
        
        <div className="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out">
          {/* Header */}
          <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
            <div className="container mx-auto px-4 py-3 flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <SidebarTrigger />
                <div className="relative">
                  <Brain className="h-8 w-8 text-primary" />
                  <Sparkles className="h-4 w-4 text-primary-glow absolute -top-1 -right-1" />
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                    RAG AI Dashboard
                  </h1>
                  <p className="text-sm text-muted-foreground">Your AI-powered knowledge companion</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <Badge variant="secondary" className="bg-gradient-card">
                  {currentMessages.length} messages
                </Badge>
                <ThemeToggle />
                <Button variant="ghost" size="icon">
                  <User className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handleLogout}
                  className="text-muted-foreground hover:text-destructive"
                >
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1 container mx-auto px-4 py-6 max-w-5xl">
            <Card className="h-[calc(100vh-8rem)] bg-gradient-card border-0 shadow-glow backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center space-x-2">
                  <Bot className="h-5 w-5 text-primary" />
                  <span>{chatSessions[currentChatId]?.title || 'New Chat'}</span>
                </CardTitle>
              </CardHeader>
              
              <CardContent className="flex flex-col h-full pb-6">
                {/* Messages Area */}
                <ScrollArea className="flex-1 mb-4 pr-4">
                  <div className="space-y-4">
                    {currentMessages.map((message) => (
                      <div
                        key={message.id}
                        className={`flex items-start space-x-3 ${
                          message.sender === "user" ? "justify-end" : "justify-start"
                        }`}
                      >
                        {message.sender === "ai" && (
                          <Avatar className="w-8 h-8 bg-gradient-primary">
                            <AvatarFallback className="bg-transparent text-primary-foreground text-xs">
                              AI
                            </AvatarFallback>
                          </Avatar>
                        )}
                        
                        <div
                          className={`max-w-[80%] rounded-lg px-4 py-3 ${
                            message.sender === "user"
                              ? "bg-primary text-primary-foreground ml-12"
                              : "bg-muted"
                          }`}
                        >
                          <div className="text-sm leading-relaxed whitespace-pre-line">{message.content}</div>
                          <p className={`text-xs mt-2 ${
                            message.sender === "user" 
                              ? "text-primary-foreground/70" 
                              : "text-muted-foreground"
                          }`}>
                            {message.timestamp.toLocaleTimeString()}
                          </p>
                        </div>

                        {message.sender === "user" && (
                          <Avatar className="w-8 h-8 bg-secondary">
                            <AvatarFallback className="text-xs">
                              U
                            </AvatarFallback>
                          </Avatar>
                        )}
                      </div>
                    ))}
                    
                    {isLoading && (
                      <div className="flex items-start space-x-3">
                        <Avatar className="w-8 h-8 bg-gradient-primary">
                          <AvatarFallback className="bg-transparent text-primary-foreground text-xs">
                            AI
                          </AvatarFallback>
                        </Avatar>
                        <div className="bg-muted rounded-lg px-4 py-3">
                          <div className="flex items-center space-x-2">
                            <Loader2 className="h-4 w-4 animate-spin" />
                            <span className="text-sm text-muted-foreground">Thinking...</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </ScrollArea>

                {/* Input Area */}
                <div className="flex space-x-2">
                  <Input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask your question..."
                    className="flex-1 bg-background/50 border-border/50 focus:border-primary transition-colors"
                    disabled={isLoading}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSubmit(e as any);
                      }
                    }}
                  />
                  <Button
                    onClick={handleSubmit}
                    disabled={isLoading || !question.trim()}
                    className="bg-gradient-primary hover:opacity-90 transition-opacity px-6"
                  >
                    {isLoading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Dashboard;