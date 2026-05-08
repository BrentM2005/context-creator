import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaFolderOpen, FaPlay, FaCopy, FaDownload } from 'react-icons/fa';
import { processFiles, type ProcessOptions } from '../utils/processor';
import { useI18n } from '../context/I18nContext';

type DirectoryInputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  webkitdirectory?: string;
  directory?: string;
};

export default function LiteApp() {
  const { t } = useI18n();
  const [files, setFiles] = useState<FileList | null>(null);
  const [progress, setProgress] = useState(0);
  const[isProcessing, setIsProcessing] = useState(false);
  const [output, setOutput] = useState('');
  const [tokenEstimate, setTokenEstimate] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  
  const [options, setOptions] = useState<ProcessOptions>({
    maxSizeKb: 500,
    extensions: '',
    removeEmptyLines: true,
    format: 'ChatGPT / Standard (Markdown)',
  });

  const handleGenerate = async () => {
    if (!files || files.length === 0) {
      alert('Please select a folder first.');
      return;
    }
    setIsProcessing(true);
    setProgress(0);
    try {
      const result = await processFiles(files, options, setProgress);
      setOutput(result);
      setTokenEstimate(Math.floor(result.length / 4));
    } catch {
      alert('Error processing files. Try a smaller directory.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-5xl mx-auto px-6 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-dark mb-2">{t('lite_title')}</h1>
        <p className="text-sm bg-yellow-50 border border-yellow-200 text-yellow-800 p-3 rounded-md">
          <strong>Note:</strong> {t('lite_note')}
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-1 space-y-6">
          <div className="bg-white p-5 rounded-xl border border-border-dark">
            <h3 className="font-bold text-sm uppercase text-text-muted mb-4 tracking-wider">
              {t('lite_step1')}
            </h3>
            <div className={`relative w-full border-2 border-dashed rounded-lg transition-all duration-200 overflow-hidden
                ${isDragging ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-primary/50 hover:border-primary bg-bg-light'}`}>
              <input
                type="file"
                title=""
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => { setFiles(e.target.files); setIsDragging(false); }}
                onDragEnter={() => setIsDragging(true)}
                onDragLeave={() => setIsDragging(false)}
                onDrop={() => setIsDragging(false)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                {...({ webkitdirectory: 'true', directory: 'true' } satisfies DirectoryInputProps)}
              />
              <div className="flex flex-col items-center justify-center gap-3 py-8 pointer-events-none">
                <FaFolderOpen className={`text-3xl transition-colors ${isDragging ? 'text-primary' : 'text-primary/70'}`} />
                <div className="text-center">
                  {files ? (
                    <p className="font-bold text-primary">{files.length} {t('lite_queued')}</p>
                  ) : (
                    <p className="font-medium text-text-dark">{t('lite_drag')}</p>
                  )}
                  {!files && <p className="text-xs text-text-muted mt-1">{t('lite_select')}</p>}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white p-5 rounded-xl border border-border-dark">
            <h3 className="font-bold text-sm uppercase text-text-muted mb-4 tracking-wider">
              {t('lite_step2')}
            </h3>
            <div className="space-y-4 text-sm">
              <div>
                <label className="block text-text-dark font-medium mb-1">{t('lite_format')}</label>
                <select className="w-full border border-border-dark rounded p-2 outline-none focus:border-primary"
                  value={options.format} onChange={(e) => setOptions({ ...options, format: e.target.value })}>
                  <option>ChatGPT / Standard (Markdown)</option>
                  <option>Claude Optimized (XML)</option>
                </select>
              </div>
              <div>
                <label className="block text-text-dark font-medium mb-1">{t('lite_ext')}</label>
                <input type="text" className="w-full border border-border-dark rounded p-2 outline-none focus:border-primary placeholder-text-muted/50"
                  value={options.extensions} onChange={(e) => setOptions({ ...options, extensions: e.target.value })} placeholder="e.g. .ts,.tsx,.py" />
              </div>
              <label className="flex items-center gap-2 cursor-pointer text-text-dark">
                <input type="checkbox" checked={options.removeEmptyLines} onChange={(e) => setOptions({ ...options, removeEmptyLines: e.target.checked })} className="accent-primary w-4 h-4" />
                {t('lite_empty')}
              </label>
            </div>
          </div>

          <button onClick={handleGenerate} disabled={isProcessing} className="w-full bg-primary hover:bg-primary-hover disabled:bg-border-dark disabled:text-text-muted text-white font-bold py-3 rounded-lg flex items-center justify-center gap-2 transition-colors shadow-sm">
            <FaPlay /> {isProcessing ? t('lite_generating') : t('lite_generate')}
          </button>
        </div>

        <div className="md:col-span-2 bg-text-dark text-border-dark p-4 rounded-xl font-mono text-sm shadow-inner flex flex-col">
          <div className="flex justify-between items-center mb-4 border-b border-gray-700 pb-2">
            <div>
              <span className="text-gray-400">Output Preview </span>
              {output && <span className="ms-2 text-xs bg-gray-800 px-2 py-1 rounded">~{tokenEstimate.toLocaleString()} tokens</span>}
            </div>
            <div className="flex gap-2">
              <button onClick={() => navigator.clipboard.writeText(output)} className="p-2 hover:bg-gray-800 rounded transition text-gray-400 hover:text-white" title="Copy">
                <FaCopy />
              </button>
              <button onClick={() => {
                  const blob = new Blob([output], { type: 'text/plain;charset=utf-8' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = options.format.includes('XML') ? 'context.xml' : 'context.md';
                  a.click();
                }} className="p-2 hover:bg-gray-800 rounded transition text-gray-400 hover:text-white" title="Download">
                <FaDownload />
              </button>
            </div>
          </div>
          {isProcessing && (
            <div className="mb-4">
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-primary transition-all duration-300" style={{ width: `${progress}%` }} />
              </div>
            </div>
          )}
          <textarea readOnly value={output || '// Ready. Load a folder and click generate.'} className="flex-1 w-full bg-transparent outline-none resize-none" dir="ltr" />
        </div>
      </div>
    </motion.div>
  );
}