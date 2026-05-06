import { motion } from 'framer-motion';
import { Link } from 'react-router';
import { FaBolt, FaTerminal, FaDesktop } from 'react-icons/fa';

export default function HomePage() {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto px-6 py-20 text-center">
      <h1 className="text-5xl font-extrabold text-text-dark mb-6 tracking-tight">
        Pack your codebase for LLMs <span className="text-primary">in seconds.</span>
      </h1>
      <p className="text-xl text-text-muted mb-12 max-w-2xl mx-auto">
        Context Creator instantly formats directories, repositories, and Pull Requests into heavily optimized Markdown or XML payloads for ChatGPT, Claude, and Gemini.
      </p>

      <div className="flex gap-4 justify-center mb-20">
        <Link to="/app" className="bg-primary hover:bg-primary-hover text-white px-8 py-3 rounded-lg font-bold transition flex items-center gap-2">
          <FaBolt /> Try Lite Version In Browser
        </Link>
        <Link to="/download" className="bg-white border border-border-dark hover:border-primary text-text-dark px-8 py-3 rounded-lg font-bold transition">
          View Downloads
        </Link>
      </div>

      <div className="grid md:grid-cols-2 gap-6 text-left">
        <div className="bg-white p-6 rounded-xl border border-border-dark shadow-sm">
          <FaDesktop className="text-primary text-2xl mb-4" />
          <h3 className="font-bold text-lg mb-2">Full Desktop GUI</h3>
          <p className="text-text-muted text-sm">Clone remote repositories, fetch GitHub/GitLab Pull requests, and bypass browser memory limitations with the PyQt6 desktop application.</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-border-dark shadow-sm">
          <FaTerminal className="text-primary text-2xl mb-4" />
          <h3 className="font-bold text-lg mb-2">Headless CLI</h3>
          <p className="text-text-muted text-sm">Integrate Context Creator directly into your shell workflow or CI/CD pipelines. Generate token-optimized payloads instantly.</p>
        </div>
      </div>
    </motion.div>
  );
}