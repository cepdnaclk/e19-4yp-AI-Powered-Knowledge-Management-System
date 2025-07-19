import { Link } from "react-router-dom"
import { Brain, Sparkles, ArrowRight, Users, Shield, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ThemeToggle } from "@/components/theme-toggle"

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-bg relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 left-20 w-64 h-64 rounded-full bg-gradient-primary blur-3xl" />
        <div className="absolute bottom-20 right-20 w-80 h-80 rounded-full bg-primary-glow/30 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-primary/10 blur-3xl" />
      </div>

      {/* Theme toggle */}
      <div className="absolute top-4 right-4 z-50">
        <ThemeToggle />
      </div>

      {/* Header */}
      <header className="relative z-10 pt-8 pb-4">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="relative">
              <Brain className="h-12 w-12 text-primary" />
              <Sparkles className="h-6 w-6 text-primary-glow absolute -top-1 -right-1" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              RAG AI
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Intelligent Question & Answer System powered by Retrieval-Augmented Generation
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold mb-6 bg-gradient-primary bg-clip-text text-transparent">
            Ask Anything, Get Intelligent Answers
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Our advanced RAG system combines the power of large language models with your custom knowledge base to provide accurate, contextual answers to any question.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button asChild size="lg" className="bg-gradient-primary hover:opacity-90 transition-opacity px-8">
              <Link to="/register">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="px-8">
              <Link to="/login">
                Sign In
              </Link>
            </Button>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <Card className="bg-gradient-card border-0 shadow-card backdrop-blur-sm hover:shadow-glow transition-all duration-300 animate-fade-in">
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-primary-foreground" />
              </div>
              <CardTitle>Intelligent Retrieval</CardTitle>
              <CardDescription>
                Advanced semantic search through your documents and knowledge base for precise information retrieval.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-gradient-card border-0 shadow-card backdrop-blur-sm hover:shadow-glow transition-all duration-300 animate-fade-in" style={{ animationDelay: "0.1s" }}>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-primary-foreground" />
              </div>
              <CardTitle>Lightning Fast</CardTitle>
              <CardDescription>
                Get answers in seconds with our optimized retrieval and generation pipeline.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="bg-gradient-card border-0 shadow-card backdrop-blur-sm hover:shadow-glow transition-all duration-300 animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-primary-foreground" />
              </div>
              <CardTitle>Secure & Reliable</CardTitle>
              <CardDescription>
                Enterprise-grade security with role-based access control and reliable performance.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* Role-based Access */}
        <div className="text-center">
          <h3 className="text-3xl font-bold mb-6">Built for Every Role</h3>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Whether you're a developer, manager, researcher, or customer support agent, our platform adapts to your specific needs.
          </p>
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {[
              { label: "Developer", icon: "💻" },
              { label: "Manager", icon: "👔" },
              { label: "Admin", icon: "🛡️" },
              { label: "Support", icon: "🎧" },
              { label: "Customer", icon: "👤" },
              { label: "Researcher", icon: "🔬" },
            ].map((role) => (
              <div key={role.label} className="flex items-center space-x-2 bg-gradient-card px-4 py-2 rounded-full border border-border/50">
                <span className="text-lg">{role.icon}</span>
                <span className="text-sm font-medium">{role.label}</span>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
