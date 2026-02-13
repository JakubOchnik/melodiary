import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authManager } from '../services/auth';
import api from '../services/api';
import type { SyncPlatformResponse } from '../types';

export const Library: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<{ userId: string; email: string } | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<SyncPlatformResponse | null>(null);
  const [syncError, setSyncError] = useState<string | null>(null);

  useEffect(() => {
    const auth = authManager.getAuthState();
    if (!auth.isAuthenticated) {
      navigate('/login');
    }

    setUser({
      userId: auth.userId || 'unknown',
      email: 'Loading...',
    });
  }, [navigate]);

  const handleLogout = () => {
    authManager.logout();
    navigate('/login');
  };

  const handleSync = async () => {
    setSyncing(true);
    setSyncResult(null);
    setSyncError(null);

    try {
      const result = await api.library.syncPlatform('spotify');
      setSyncResult(result);
      // TODO: Refresh library/track list after successful sync
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to sync library';
      setSyncError(message);
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-slate-600">Melodiary</h1>
          <button
            onClick={handleLogout}
            className="text-gray-600 hover:text-gray-900 font-medium"
            type="button"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Welcome Message */}
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Library</h2>
            <p className="text-gray-600">Sync your Spotify library to get started.</p>
            {user && <p className="text-sm text-gray-500 mt-2">User ID: {user.userId}</p>}
          </div>

          {/* Sync Section */}
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Spotify Library</h3>
                <p className="text-sm text-gray-500">
                  Import your saved tracks from Spotify into Melodiary.
                </p>
              </div>
              <button
                onClick={handleSync}
                disabled={syncing}
                className="bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium py-2 px-5 rounded-lg transition-colors"
                type="button"
              >
                {syncing ? 'Syncing...' : 'Sync Library'}
              </button>
            </div>

            {/* Sync Result */}
            {syncResult && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-green-800 font-medium">{syncResult.message}</p>
                {syncResult.malformed > 0 && (
                  <p className="text-green-700 text-sm mt-1">
                    {syncResult.malformed} track(s) could not be processed.
                  </p>
                )}
              </div>
            )}

            {/* Sync Error */}
            {syncError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800 font-medium">Sync failed</p>
                <p className="text-red-700 text-sm mt-1">{syncError}</p>
              </div>
            )}
          </div>

          {/* Placeholder for track list */}
          <div className="bg-white rounded-lg shadow p-8 text-center text-gray-400">
            <p>Track list will appear here after syncing. (TODO)</p>
          </div>
        </div>
      </main>
    </div>
  );
};
