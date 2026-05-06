import { FaWindows, FaLinux, FaTerminal } from 'react-icons/fa';
import type { DownloadCard } from '../types/download';
import type { DownloadItem } from '../types/download'; 

export function buildDownloadCards(downloads: DownloadItem[]): DownloadCard[] {
  return [
    {
      ...downloads[0],
      icon: <FaWindows className="text-[#0078D4]" />,
      desc: 'Full PyQt6 interface with Git & PR support for Windows.',
      tag: '.exe',
    },
    {
      ...downloads[1],
      icon: <FaLinux className="text-[#FCC624]" />,
      desc: 'Full PyQt6 interface with Git & PR support for Linux.',
      tag: 'Binary',
    },
    {
      ...downloads[2],
      icon: <FaTerminal className="text-gray-700" />,
      desc: 'Headless binary for Windows environments.',
      tag: '.exe',
    },
    {
      ...downloads[3],
      icon: <FaTerminal className="text-gray-700" />,
      desc: 'Headless binary for Linux environments.',
      tag: 'Binary',
    },
  ];
}