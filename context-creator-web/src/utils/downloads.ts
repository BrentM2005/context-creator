import { FaWindows, FaLinux, FaTerminal } from 'react-icons/fa';

const BASE =
  'https://github.com/BrentM2005/context-creator/releases/latest/download';

export const downloadCards = [
  {
    title: 'Windows GUI',
    icon: FaWindows,
    desc: 'Full PyQt6 interface with Git & PR support.',
    tag: '.exe (64-bit)',
    file: `${BASE}/ContextCreator.exe`,
  },
  {
    title: 'Linux GUI',
    icon: FaLinux,
    desc: 'Native Linux UI build.',
    tag: 'Binary',
    file: `${BASE}/ContextCreator`,
  },
  {
    title: 'Windows CLI',
    icon: FaTerminal,
    desc: 'Headless binary for Windows environments.',
    tag: '.exe (CLI)',
    file: `${BASE}/context-creator.exe`,
  },
  {
    title: 'Linux CLI',
    icon: FaTerminal,
    desc: 'Headless binary for CI/CD pipelines.',
    tag: 'Binary',
    file: `${BASE}/context-creator`,
  },
];