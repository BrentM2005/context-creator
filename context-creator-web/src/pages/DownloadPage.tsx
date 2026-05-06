import { motion } from 'framer-motion';
import { FaWindows, FaLinux, FaTerminal } from 'react-icons/fa';
import { useLatestRelease } from '../hooks/useLatestRelease';
import { mapAssetsToDownloads } from '../utils/mapAssets';
import type { DownloadCard } from '../types/download';

export default function DownloadPage() {
  const { release, loading, error } = useLatestRelease();

  if (loading) {
    return <div className="text-center py-20">Loading downloads...</div>;
  }

  if (error || !release) {
    return <div className="text-center py-20">Failed to load downloads</div>;
  }

  const downloads = mapAssetsToDownloads(release.assets);

  const cards: DownloadCard[] = [
    {
      ...downloads[0],
      icon: <FaWindows />,
      desc: 'Full PyQt6 interface with Git & PR support.',
      tag: '.exe (64-bit)',
    },
    {
      ...downloads[1],
      icon: <FaLinux />,
      desc: 'Native Linux UI build.',
      tag: 'Binary',
    },
    {
      ...downloads[2],
      icon: <FaTerminal />,
      desc: 'Headless binary for Windows environments.',
      tag: '.exe (CLI)',
    },
    {
      ...downloads[3],
      icon: <FaTerminal />,
      desc: 'Headless binary for CI/CD pipelines.',
      tag: 'Binary',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-5xl mx-auto px-6 py-16"
    >
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold mb-4">
          Download Context Creator
        </h1>
        <p className="text-sm text-gray-500">
          Latest version: {release.tag_name}
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map(card => (
          <div
            key={card.key}
            className="bg-white border rounded-xl p-6 flex flex-col"
          >
            <div className="text-3xl mb-4">{card.icon}</div>
            <h3 className="font-bold mb-2">{card.title}</h3>
            <p className="text-sm mb-6 flex-1">{card.desc}</p>

            <a
              href={card.file}
              className="text-center border py-2 rounded font-bold hover:bg-black hover:text-white transition"
            >
              Download {card.tag}
            </a>
          </div>
        ))}
      </div>
    </motion.div>
  );
}