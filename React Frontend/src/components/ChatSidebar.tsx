import { useState } from "react"
import { MessageSquare, Plus, Trash2, MoreHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  useSidebar,
} from "@/components/ui/sidebar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export interface ChatSession {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  messageCount: number
}

interface ChatSidebarProps {
  currentChatId?: string
  onChatSelect: (chatId: string) => void
  onNewChat: () => void
  onDeleteChat: (chatId: string) => void
}

export function ChatSidebar({ 
  currentChatId, 
  onChatSelect, 
  onNewChat, 
  onDeleteChat 
}: ChatSidebarProps) {
  const { state } = useSidebar()
  const collapsed = state === "collapsed"
  
  // Placeholder data - replace with your database queries
  const [chatSessions] = useState<ChatSession[]>([
    {
      id: "1",
      title: "Python Data Analysis",
      lastMessage: "How to analyze CSV files with pandas?",
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 min ago
      messageCount: 8
    },
    {
      id: "2", 
      title: "React Best Practices",
      lastMessage: "What are the latest React patterns?",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
      messageCount: 12
    },
    {
      id: "3",
      title: "Machine Learning Basics",
      lastMessage: "Explain neural networks simply",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
      messageCount: 5
    }
  ])

  const formatTime = (date: Date) => {
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return "now"
    if (diffInHours < 24) return `${diffInHours}h`
    return `${Math.floor(diffInHours / 24)}d`
  }

  const truncateText = (text: string, maxLength: number) => {
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text
  }

  return (
    <Sidebar className={collapsed ? "w-16" : "w-80"}>
      <SidebarHeader className="p-4">
        <Button 
          onClick={onNewChat}
          className="w-fit bg-gradient-primary hover:bg-primary/90 text-white"
        >
          <Plus className="h-4 w-4" />
          {!collapsed && <span className="ml-2">New Chat</span>}
        </Button>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className={collapsed ? "sr-only" : ""}>
            Recent Chats
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {chatSessions.map((chat) => (
                <SidebarMenuItem key={chat.id}>
                  <div className="group relative">
                    <SidebarMenuButton
                      onClick={() => onChatSelect(chat.id)}
                      className={`w-full p-3 text-left transition-all duration-200 ${
                        currentChatId === chat.id 
                          ? "bg-primary/10 border-l-2 border-primary" 
                          : "hover:bg-accent/50"
                      }`}
                    >
                      <div className="flex items-start space-x-3">
                        <MessageSquare className="h-4 w-4 mt-1 flex-shrink-0 text-primary" />
                        {!collapsed && (
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between">
                              <h4 className="text-sm font-medium truncate">
                                {truncateText(chat.title, 20)}
                              </h4>
                              <span className="text-xs text-muted-foreground">
                                {formatTime(chat.timestamp)}
                              </span>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1 truncate">
                              {truncateText(chat.lastMessage, 35)}
                            </p>
                            <div className="flex items-center justify-between mt-2">
                              <span className="text-xs text-muted-foreground">
                                {chat.messageCount} messages
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    </SidebarMenuButton>
                    
                    {!collapsed && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="absolute top-2 right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                          >
                            <MoreHorizontal className="h-3 w-3" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem 
                            onClick={() => onDeleteChat(chat.id)}
                            className="text-destructive"
                          >
                            <Trash2 className="h-4 w-4 mr-2 " />
                            Delete Chat
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                  </div>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}