import { Link, useLocation } from 'react-router';
import { FaLayerGroup, FaGithub } from 'react-icons/fa';

export default function Navbar() {
  const location = useLocation();

  const links =[
    { name: 'Home', path: '/' },
    { name: 'Web Version', path: '/app' },
    { name: 'Downloads', path: '/download' },
  ];

  return (
    <nav className="border-b border-border-dark bg-white/95 sticky top-0 z-50 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-text-dark font-bold text-xl tracking-tight">
          <FaLayerGroup className="text-primary text-2xl" />
          Context Creator
        </Link>
        <div className="flex items-center gap-6">
          {links.map(link => (
            <Link 
              key={link.path} 
              to={link.path}
              className={`font-medium transition-colors ${location.pathname === link.path ? 'text-primary' : 'text-text-muted hover:text-text-dark'}`}
            >
              {link.name}
            </Link>
          ))}
          <a href="https://github.com/BrentM2005/context-creator" target="_blank" rel="noreferrer" className="text-text-muted hover:text-text-dark transition-colors">
            <FaGithub className="text-2xl" />
          </a>
        </div>
      </div>
    </nav>
  );
}