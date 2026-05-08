import { Link, useLocation } from 'react-router';
import { FaLayerGroup, FaGithub, FaGlobe } from 'react-icons/fa';
import { useI18n } from '../context/I18nContext';
import type { Language } from '../i18n/translations';

export default function Navbar() {
  const location = useLocation();
  const { lang, setLang, t } = useI18n();

  const links =[
    { name: t('nav_home'), path: '/' },
    { name: t('nav_web'), path: '/app' },
    { name: t('nav_dl'), path: '/download' },
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
          
          <div className="relative group flex items-center text-text-muted hover:text-text-dark transition-colors cursor-pointer">
            <FaGlobe className="text-xl" />
            <select 
              value={lang} 
              onChange={(e) => setLang(e.target.value as Language)}
              className="absolute inset-0 opacity-0 cursor-pointer"
            >
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="pt">Português</option>
              <option value="de">Deutsch</option>
              <option value="ja">日本語</option>
              <option value="zh">中文</option>
              <option value="ar">العربية</option>
              <option value="hi">हिन्दी</option>
            </select>
          </div>

          <a href="https://github.com/BrentM2005/context-creator" target="_blank" rel="noreferrer" className="text-text-muted hover:text-text-dark transition-colors">
            <FaGithub className="text-2xl" />
          </a>
        </div>
      </div>
    </nav>
  );
}