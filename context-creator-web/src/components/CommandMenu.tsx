import { useEffect, useState } from 'react';
import { Command } from 'cmdk';
import { useNavigate } from 'react-router';
import { FaHome, FaPlay, FaDownload, FaGithub } from 'react-icons/fa';

export default function CommandMenu() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  },[]);

  const runCommand = (command: () => void) => {
    setOpen(false);
    command();
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-textDark/20 backdrop-blur-sm z-50 flex items-start justify-center pt-[20vh]">
      <Command className="bg-white rounded-xl shadow-2xl border border-borderDark w-full max-w-lg overflow-hidden" loop>
        <Command.Input placeholder="Type a command or search..." className="w-full px-4 py-4 outline-none border-b border-borderDark text-textDark" />
        <Command.List className="p-2 max-h-75 overflow-y-auto">
          <Command.Empty className="p-4 text-center text-textMuted">No results found.</Command.Empty>
          <Command.Group heading="Navigation" className="text-xs font-semibold text-textMuted px-2 py-1">
            <Command.Item onSelect={() => runCommand(() => navigate('/'))} className="flex items-center gap-2 px-3 py-2 mt-1 rounded-md cursor-pointer hover:bg-bgLight text-sm text-textDark aria-selected:bg-primary aria-selected:text-white">
              <FaHome /> Home
            </Command.Item>
            <Command.Item onSelect={() => runCommand(() => navigate('/app'))} className="flex items-center gap-2 px-3 py-2 mt-1 rounded-md cursor-pointer hover:bg-bgLight text-sm text-textDark aria-selected:bg-primary aria-selected:text-white">
              <FaPlay /> Open Web Version
            </Command.Item>
            <Command.Item onSelect={() => runCommand(() => navigate('/download'))} className="flex items-center gap-2 px-3 py-2 mt-1 rounded-md cursor-pointer hover:bg-bgLight text-sm text-textDark aria-selected:bg-primary aria-selected:text-white">
              <FaDownload /> Downloads
            </Command.Item>
            <Command.Item onSelect={() => runCommand(() => window.open('https://github.com/BrentM2005/context-creator', '_blank'))} className="flex items-center gap-2 px-3 py-2 mt-1 rounded-md cursor-pointer hover:bg-bgLight text-sm text-textDark aria-selected:bg-primary aria-selected:text-white">
              <FaGithub /> GitHub
            </Command.Item>
          </Command.Group>
        </Command.List>
      </Command>
    </div>
  );
}