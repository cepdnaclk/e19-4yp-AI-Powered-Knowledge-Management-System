import { useState } from "react"
import { Send, Brain, Sparkles, LogOut, User, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { ThemeToggle } from "@/components/theme-toggle"
import { useToast } from "@/hooks/use-toast"

interface Message {
  id: string
  content: string
  sender: "user" | "ai"
  timestamp: Date
}

export default function Dashboard() {
  const [question, setQuestion] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Hello! I'm your RAG AI assistant. I can help answer questions based on your knowledge base. What would you like to know?",
      sender: "ai",
      timestamp: new Date()
    }
  ])
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: question,
      sender: "user",
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setQuestion("")
    setIsLoading(true)

    try {
      // TODO: Integrate with your Flask RAG backend
      console.log("Sending question to RAG model:", question)
      
      // Simulate API call to your RAG endpoint
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: `Based on the knowledge base, here's what I found regarding "${userMessage.content}": This is a simulated response. Your RAG model would provide the actual answer based on your document embeddings and retrieval system.`,
        sender: "ai",
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiResponse])
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to get response. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    // TODO: Implement logout logic
    toast({
      title: "Logged out",
      description: "You have been logged out successfully.",
    })
  }

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Brain className="h-8 w-8 text-primary" />
              <Sparkles className="h-4 w-4 text-primary-glow absolute -top-1 -right-1" />
            </div>
            <h1 className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              RAG AI Dashboard
            </h1>
          </div>
          
          <div className="flex items-center space-x-3">
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
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <Card className="h-[calc(100vh-8rem)] bg-gradient-card border-0 shadow-glow backdrop-blur-sm">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-primary" />
              AI Question & Answer
            </CardTitle>
          </CardHeader>
          
          <CardContent className="flex flex-col h-full pb-6">
            {/* Messages Area */}
            <ScrollArea className="flex-1 mb-4 pr-4">
              <div className="space-y-4">
                {messages.map((message) => (
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
                      <p className="text-sm leading-relaxed">{message.content}</p>
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
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="flex space-x-2">
              <Input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask your question..."
                className="flex-1 bg-background/50 border-border/50 focus:border-primary transition-colors"
                disabled={isLoading}
              />
              <Button
                type="submit"
                disabled={isLoading || !question.trim()}
                className="bg-gradient-primary hover:opacity-90 transition-opacity px-6"
              >
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}