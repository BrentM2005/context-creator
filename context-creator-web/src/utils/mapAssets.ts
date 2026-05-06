import type { GitHubAsset } from '../types/GitHub';
import type { DownloadItem } from '../types/download';

export function mapAssetsToDownloads(
  assets: GitHubAsset[]
): DownloadItem[] {
  const find = (namePart: string): string | undefined =>
    assets.find(a => a.name.includes(namePart))?.browser_download_url;

  return [
    {
      title: 'Windows GUI',
      key: 'win-gui',
      file: find('GUI-Windows'),
    },
    {
      title: 'Linux GUI',
      key: 'linux-gui',
      file: find('GUI-Linux'),
    },
    {
      title: 'Windows CLI',
      key: 'win-cli',
      file: find('CLI-Windows'),
    },
    {
      title: 'Linux CLI',
      key: 'linux-cli',
      file: find('CLI-Linux'),
    },
  ];
}