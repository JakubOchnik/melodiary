import { useCallback, useEffect, useState } from 'react';
import api from '../../services/api';
import type { Track } from '../../types';
import { TrackItem } from './TrackItem';

interface TrackListProps {
  refreshKey: number;
}

export const TrackList: React.FC<TrackListProps> = ({ refreshKey }) => {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [lastKey, setLastKey] = useState<Record<string, string> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = useCallback(async (trackId: string) => {
    await api.library.deleteTrack(trackId);
    setTracks((prev) => prev.filter((t) => t.trackId !== trackId));
  }, []);

  const fetchTracks = useCallback(async (cursor?: Record<string, string> | null) => {
    setLoading(true);
    setError(null);

    try {
      const params: { limit: number; lastKey?: string } = { limit: 50 };
      if (cursor) {
        params.lastKey = JSON.stringify(cursor);
      }
      const result = await api.library.getLibrary(params);
      setTracks((prev) => (cursor ? [...prev, ...result.items] : result.items));
      setLastKey(result.lastKey);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load library';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setTracks([]);
    setLastKey(null);
    fetchTracks();
  }, [fetchTracks, refreshKey]);

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900">
          Your Tracks{tracks.length > 0 && ` (showing ${tracks.length})`}
        </h3>
      </div>

      {error && (
        <div className="p-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        </div>
      )}

      {!loading && tracks.length === 0 && !error && (
        <div className="p-8 text-center text-gray-400">
          <p>No tracks yet. Sync your Spotify library to get started.</p>
        </div>
      )}

      {tracks.length > 0 && (
        <ul className="divide-y divide-gray-100">
          {tracks.map((track) => (
            <TrackItem key={track.trackId} track={track} onDelete={handleDelete} />
          ))}
        </ul>
      )}

      {lastKey && (
        <div className="p-4 border-t border-gray-100 text-center">
          <button
            onClick={() => fetchTracks(lastKey)}
            disabled={loading}
            className="text-slate-600 hover:text-slate-800 font-medium text-sm disabled:text-gray-400"
            type="button"
          >
            {loading ? 'Loading...' : 'Load more tracks'}
          </button>
        </div>
      )}

      {loading && tracks.length === 0 && (
        <div className="p-8 text-center text-gray-400">
          <p>Loading tracks...</p>
        </div>
      )}
    </div>
  );
};
