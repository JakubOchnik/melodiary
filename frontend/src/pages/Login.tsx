import { useState } from 'react';
import api from '../services/api';

export const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const handleSpotifyLogin = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get Spotify auth URL from backend
      const authUrl = await api.auth.getSpotifyAuthUrl();

      // Redirect to Spotify auth page
      window.location.href = authUrl;
    } catch (err) {
      console.error('Error during Spotify login:', err);
      setError('Failed to connect to Spotify. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-500 to-slate-800 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2">Melodiary</h1>
          <p className="text-gray-300">Your music, all in one place</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Sign in to continue</h2>

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Spotify Login Button */}
          <button
            onClick={handleSpotifyLogin}
            disabled={loading}
            className="w-full bg-[#1DB954] hover:bg-[#1ed760] text-white font-semibold py-4 px-6 rounded-lg transition-colors flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            type="button"
          >
            {loading ? (
              <>
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <span>Connecting...</span>
              </>
            ) : (
              <>
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
                </svg>
                <span>Continue with Spotify</span>
              </>
            )}
          </button>

          {/* Additional Info */}
          <div className="mt-6 text-center text-sm text-gray-600">
            <p>By continuing, you agree to connect your Spotify account to Melodiary.</p>
          </div>

          {/* Other platforms info */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-center text-sm text-gray-500 mb-4">More platforms coming soon</p>
            <div className="flex justify-center gap-4 opacity-50">
              <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  viewBox="0 0 16 16"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="m10.995 0 .573.001q.241 0 .483.007c.35.01.705.03 1.051.093.352.063.68.166.999.329a3.36 3.36 0 0 1 1.47 1.468c.162.32.265.648.328 1 .063.347.084.7.093 1.051q.007.241.007.483l.001.573v5.99l-.001.573q0 .241-.008.483c-.01.35-.03.704-.092 1.05a3.5 3.5 0 0 1-.33 1 3.36 3.36 0 0 1-1.468 1.468 3.5 3.5 0 0 1-1 .33 7 7 0 0 1-1.05.092q-.241.007-.483.008l-.573.001h-5.99l-.573-.001q-.241 0-.483-.008a7 7 0 0 1-1.052-.092 3.6 3.6 0 0 1-.998-.33 3.36 3.36 0 0 1-1.47-1.468 3.6 3.6 0 0 1-.328-1 7 7 0 0 1-.093-1.05Q.002 11.81 0 11.568V5.005l.001-.573q0-.241.007-.483c.01-.35.03-.704.093-1.05a3.6 3.6 0 0 1 .329-1A3.36 3.36 0 0 1 1.9.431 3.5 3.5 0 0 1 2.896.1 7 7 0 0 1 3.95.008Q4.19.002 4.432 0h.573zm-.107 2.518-4.756.959H6.13a.66.66 0 0 0-.296.133.5.5 0 0 0-.16.31c-.004.027-.01.08-.01.16v5.952c0 .14-.012.275-.106.39-.095.115-.21.15-.347.177l-.31.063c-.393.08-.65.133-.881.223a1.4 1.4 0 0 0-.519.333 1.25 1.25 0 0 0-.332.995c.031.297.166.582.395.792.156.142.35.25.578.296.236.047.49.031.858-.043.196-.04.38-.102.555-.205a1.4 1.4 0 0 0 .438-.405 1.5 1.5 0 0 0 .233-.55c.042-.202.052-.386.052-.588V6.347c0-.276.08-.35.302-.404.024-.005 3.954-.797 4.138-.833.257-.049.378.025.378.294v3.524c0 .14-.001.28-.096.396-.094.115-.211.15-.348.178l-.31.062c-.393.08-.649.133-.88.223a1.4 1.4 0 0 0-.52.334 1.26 1.26 0 0 0-.34.994c.03.297.174.582.404.792a1.2 1.2 0 0 0 .577.294c.237.048.49.03.858-.044.197-.04.381-.098.556-.202a1.4 1.4 0 0 0 .438-.405q.173-.252.233-.549a2.7 2.7 0 0 0 .044-.589V2.865c0-.273-.143-.443-.4-.42-.04.003-.383.064-.424.073"
                  />
                </svg>
              </div>
              <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                <svg
                  version="1.1"
                  id="Layer_1"
                  width="16"
                  height="16"
                  viewBox="0 0 176 176"
                  enableBackground="new 0 0 176 176"
                  aria-hidden="true"
                >
                  <g id="XMLID_167_">
                    <circle id="XMLID_791_" fill="#FF0000" cx="88" cy="88" r="88" />
                    <path
                      id="XMLID_42_"
                      fill="#FFFFFF"
                      d="M88,46c23.1,0,42,18.8,42,42s-18.8,42-42,42s-42-18.8-42-42S64.9,46,88,46 M88,42   c-25.4,0-46,20.6-46,46s20.6,46,46,46s46-20.6,46-46S113.4,42,88,42L88,42z"
                    />
                    <polygon id="XMLID_274_" fill="#FFFFFF" points="72,111 111,87 72,65  " />
                  </g>
                </svg>
              </div>
              <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                {/*Tidal*/}
                📻
              </div>
            </div>
          </div>
        </div>
        {/* Footer */}
        <p className="text-center text-gray-400 text-sm mt-8">
          Don't have a Spotify account?{' '}
          <a
            href="https://www.spotify.com/signup"
            target="_blank"
            rel="noopener noreferrer"
            className="text-white hover:underline"
          >
            Sign up here
          </a>
        </p>
      </div>
    </div>
  );
};
