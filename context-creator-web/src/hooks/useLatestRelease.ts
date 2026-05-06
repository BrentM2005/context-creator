import { useEffect, useState } from 'react';
import type { GitHubRelease } from '../types/GitHub';

export function useLatestRelease() {
  const [release, setRelease] = useState<GitHubRelease | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('https://api.github.com/repos/BrentM2005/context-creator/releases/latest')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch release');
        return res.json();
      })
      .then((data: GitHubRelease) => {
        setRelease(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { release, loading, error };
}