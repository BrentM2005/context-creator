import { useEffect, useState } from 'react';
import type { GitHubRelease } from '../types/github';

export function useReleases() {
  const[releases, setReleases] = useState<GitHubRelease[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

   useEffect(() => {
    fetch('https://api.github.com/repos/BrentM2005/context-creator/releases')
      .then(res => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setReleases(data);
        } else {
          setError(data.message || 'Failed to fetch releases');
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  },[]);

  return { releases, loading, error };
}