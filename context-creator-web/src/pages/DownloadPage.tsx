import { useState } from 'react';
import { motion } from 'framer-motion';
import { useReleases } from '../hooks/useReleases';
import { mapAssetsToDownloads } from '../utils/mapAssets';
import { buildDownloadCards } from '../utils/buildDownloadCards';

export default function DownloadPage() {
  const { releases, loading, error } = useReleases();
  const [selectedVersionId, setSelectedVersionId] = useState<number | null>(null);

  const activeVersionId = selectedVersionId ?? releases[0]?.id ?? null;

  if (loading) {
    return <div className="text-center py-20 text-lg font-medium text-text-muted animate-pulse">Loading downloads...</div>;
  }

  if (error || releases.length === 0) {
    return <div className="text-center py-20 text-lg text-red-500">Failed to load downloads or no releases found.</div>;
  }

  const selectedRelease = releases.find(r => r.id === activeVersionId) || releases[0];
  const downloads = mapAssetsToDownloads(selectedRelease.assets);
  const cards = buildDownloadCards(downloads);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-6xl mx-auto px-6 py-16"
    >
      <div className="text-center mb-16 flex flex-col items-center">
        <h1 className="text-4xl font-extrabold mb-6 text-text-dark">
          Download Context Creator
        </h1>
        
        {/* Version Dropdown */}
        <div className="flex items-center gap-3 bg-white border border-border-dark py-2 px-4 rounded-lg shadow-sm">
          <label htmlFor="version-select" className="text-sm font-semibold text-text-muted uppercase tracking-wide">
            Version:
          </label>
          <select
            id="version-select"
            value={activeVersionId ?? ''}
            onChange={(e) => setSelectedVersionId(Number(e.target.value))}
            className="bg-transparent text-text-dark font-bold text-lg outline-none cursor-pointer focus:ring-0"
          >
            {releases.map(r => (
              <option key={r.id} value={r.id}>
                {r.tag_name} {r.id === releases[0].id ? '(Latest)' : ''}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        {cards.map(card => (
          <div
            key={card.key}
            className="bg-white border border-border-dark rounded-2xl p-8 flex flex-col hover:border-primary hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden group"
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-border-dark to-transparent group-hover:via-primary transition-all duration-300"></div>
            
            <div className="text-5xl mb-6 flex justify-center drop-shadow-sm group-hover:scale-110 transition-transform duration-300">
              {card.icon}
            </div>
            
            <h3 className="font-extrabold text-xl mb-3 text-center text-text-dark">{card.title}</h3>
            <p className="text-text-muted text-center mb-8 flex-1 leading-relaxed text-sm">{card.desc}</p>

            <a
              href={card.file || '#'}
              onClick={(e) => {
                if (!card.file) e.preventDefault();
              }}
              className={`flex items-center justify-center py-3 px-4 rounded-xl font-bold transition-all duration-200 shadow-sm ${
                card.file 
                  ? 'bg-primary text-white hover:bg-primary-hover hover:shadow-md' 
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
              }`}
            >
              {card.file ? `Download ${card.tag}` : 'Not Available'}
            </a>
          </div>
        ))}
      </div>

      {selectedRelease?.body && (
        <div className="mt-16 max-w-4xl mx-auto bg-white border border-border-dark rounded-2xl p-8 shadow-sm">
          <h3 className="text-xl font-bold mb-4 border-b border-border-dark pb-3 text-text-dark">Release Notes ({selectedRelease.tag_name})</h3>
          <div className="prose prose-slate max-w-none text-text-muted whitespace-pre-wrap text-sm leading-relaxed">
            {selectedRelease.body}
          </div>
        </div>
      )}
    </motion.div>
  );
}