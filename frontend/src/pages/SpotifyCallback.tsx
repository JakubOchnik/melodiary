import { useEffect, useState, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../services/api';
import { authManager } from '../services/auth';

export const SpotifyCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Prevent double execution in React Strict Mode
    if (hasProcessed.current) {
      return;
    }
    hasProcessed.current = true;

    const handleCallback = async () => {
      // Get auth code from URL
      const code = searchParams.get('code');
      const error = searchParams.get('error');

      if (error) {
        setStatus('error');
        setErrorMessage(`Spotify authorization error: ${error}`);
        setTimeout(() => navigate('/login'), 5000);
        return;
      }

      if (!code) {
        setStatus('error');
        setErrorMessage('No authorization code received from Spotify.');
        setTimeout(() => navigate('/login'), 5000);
        return;
      }

      try {
        console.log('Received Spotify auth code');
        // Exchange code for token
        const response = await api.auth.spotifyCallback(code);

        authManager.setAuth(response.token, response.user.userId);
        setStatus('success');

        setTimeout(() => navigate('/library'), 1500);
      } catch (err: any) {
        console.error('Callback handling error:', err);
        setStatus('error');
        setErrorMessage(err.response?.data?.error || 'Failed to authenticate. Please try again.');
        setTimeout(() => navigate('/login'), 5000);
      }
    };

    handleCallback();
  }, [searchParams, navigate]);
  return (
    <div className="min-h-screen bg-linear-to-br from-slate-500 to-slate-800 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8 text-center">
        {status === 'loading' && (
          <>
            <div className="mb-6">
              <svg
                className="animate-spin h-16 w-16 text-purple-600 mx-auto"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
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
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Connecting your account...</h2>
            <p className="text-gray-600">Please wait a moment</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="mb-6 text-6xl">✅</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Successfully connected!</h2>
            <p className="text-gray-600">Redirecting to your library...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="mb-6 text-6xl">❌</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Connection failed</h2>
            <p className="text-gray-600 mb-4">{errorMessage}</p>
            <p className="text-sm text-gray-500">Redirecting to login...</p>
          </>
        )}
      </div>
    </div>
  );
};
