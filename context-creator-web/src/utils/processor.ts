export const IGNORED_DIRS = new Set([
  'node_modules', '.git', '.venv', 'venv', '__pycache__', 'build', 'dist', 
  '.next', '.nuxt', 'coverage', '.cache', 'vendor', 'target', 'bin', 'obj'
]);

export const IGNORED_FILES = new Set([
  'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 
  '.DS_Store', 'Thumbs.db', '.env', '.gitignore'
]);

export interface ProcessOptions {
  maxSizeKb: number;
  extensions: string;
  removeEmptyLines: boolean;
  format: string;
}

export async function processFiles(files: FileList, options: ProcessOptions, onProgress: (p: number) => void): Promise<string> {
  const extList = options.extensions.split(',').map(e => e.trim().toLowerCase()).filter(Boolean);
  let output = '';
  
  if (options.format === 'Claude Optimized (XML)') {
    output += `<repository_documents>\n`;
  } else {
    output += `# Context Creator (Web Lite)\n\n## Files\n\n`;
  }

  const validFiles: File[] =[];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const pathParts = file.webkitRelativePath.split('/');
    
    if (pathParts.some(part => IGNORED_DIRS.has(part))) continue;
    if (IGNORED_FILES.has(file.name)) continue;
    if (file.size > options.maxSizeKb * 1024) continue;
    
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (extList.length > 0 && !extList.includes(ext)) continue;

    validFiles.push(file);
  }

  for (let i = 0; i < validFiles.length; i++) {
    const file = validFiles[i];
    let content = await file.text();

    if (options.removeEmptyLines) {
      content = content.split('\n').filter(line => line.trim().length > 0).join('\n');
    }

    if (options.format === 'Claude Optimized (XML)') {
      output += `<document index="${i + 1}">\n<source>${file.webkitRelativePath}</source>\n<document_content>\n${content}\n</document_content>\n</document>\n\n`;
    } else {
      output += `### \`${file.webkitRelativePath}\`\n\`\`\`\n${content}\n\`\`\`\n\n`;
    }

    onProgress(((i + 1) / validFiles.length) * 100);
  }

  if (options.format === 'Claude Optimized (XML)') {
    output += `</repository_documents>\n`;
  }

  return output;
}