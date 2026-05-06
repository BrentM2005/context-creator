import type { GitHubAsset } from '../types/github';
import type { DownloadItem } from '../types/download';

export function mapAssetsToDownloads(
  assets: GitHubAsset[]
): DownloadItem[] {
  const find = (exactName: string): string | undefined =>
    assets.find(a => a.name === exactName)?.browser_download_url;

  return[
    {
      title: 'Windows GUI',
      key: 'win-gui',
      file: find('ContextCreator.exe'),
    },
    {
      title: 'Linux GUI',
      key: 'linux-gui',
      file: find('ContextCreator'),
    },
    {
      title: 'Windows CLI',
      key: 'win-cli',
      file: find('context-creator.exe'),
    },
    {
      title: 'Linux CLI',
      key: 'linux-cli',
      file: find('context-creator'),
    },
  ];
}