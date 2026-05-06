import type { ReactNode } from 'react';

export interface DownloadItem {
  title: string;
  key: string;
  file?: string;
}

export interface DownloadCard extends DownloadItem {
  icon: ReactNode;
  desc: string;
  tag: string;
}