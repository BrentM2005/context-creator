import { motion } from 'framer-motion';
import { Link } from 'react-router';
import { FaBolt, FaTerminal, FaDesktop } from 'react-icons/fa';
import { useI18n } from '../context/I18nContext';

export default function HomePage() {
  const { t } = useI18n();
  
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto px-6 py-20 text-center">
      <h1 className="text-5xl font-extrabold text-text-dark mb-6 tracking-tight">
        {t('hero_title_1')} <span className="text-primary">{t('hero_title_2')}</span>
      </h1>
      <p className="text-xl text-text-muted mb-12 max-w-2xl mx-auto">
        {t('hero_desc')}
      </p>
      <div className="flex gap-4 justify-center mb-20">
        <Link to="/app" className="bg-primary hover:bg-primary-hover text-white px-8 py-3 rounded-lg font-bold transition flex items-center gap-2">
          <FaBolt /> {t('btn_try')}
        </Link>
        <Link to="/download" className="bg-white border border-border-dark hover:border-primary text-text-dark px-8 py-3 rounded-lg font-bold transition">
          {t('btn_dl')}
        </Link>
      </div>
      <div className="grid md:grid-cols-2 gap-6 text-start">
        <div className="bg-white p-6 rounded-xl border border-border-dark shadow-sm">
          <FaDesktop className="text-primary text-2xl mb-4" />
          <h3 className="font-bold text-lg mb-2">{t('feat_desktop')}</h3>
          <p className="text-text-muted text-sm">{t('feat_desktop_desc')}</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-border-dark shadow-sm">
          <FaTerminal className="text-primary text-2xl mb-4" />
          <h3 className="font-bold text-lg mb-2">{t('feat_cli')}</h3>
          <p className="text-text-muted text-sm">{t('feat_cli_desc')}</p>
        </div>
      </div>
    </motion.div>
  );
}