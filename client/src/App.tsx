import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch, Router as WouterRouter } from "wouter";
import { useHashLocation } from "wouter/use-hash-location";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/404" component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  // Hook nativo do wouter para gerenciar rotas via Hash (#/) no GitHub Pages
  const [location, setLocation] = useHashLocation();

  return (
    <ThemeProvider defaultTheme="light">
      <TooltipProvider>
        <Toaster />
        <ErrorBoundary>
          <WouterRouter hook={useHashLocation}>
            <Router />
          </WouterRouter>
        </ErrorBoundary>
      </TooltipProvider>
    </ThemeProvider>
  );
}

export default App;
