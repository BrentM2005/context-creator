import { BrowserRouter as Router, Routes, Route } from 'react-router';
import Navbar from './components/Navbar';
import CommandMenu from './components/CommandMenu';
import HomePage from './pages/HomePage';
import LiteAppPage from './pages/LiteAppPage';
import DownloadPage from './pages/DownloadPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-bgLight font-sans text-textDark flex flex-col">
        <Navbar />
        <CommandMenu />
        
        <div className="fixed bottom-4 right-4 bg-white border border-borderDark px-3 py-1.5 rounded-full shadow-sm text-xs text-textMuted font-medium z-40 hidden md:block">
          Press <kbd className="bg-bgLight px-1.5 py-0.5 rounded border border-borderDark font-mono">Cmd + K</kbd>
        </div>

        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/app" element={<LiteAppPage />} />
            <Route path="/download" element={<DownloadPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;