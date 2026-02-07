import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authManager } from '../services/auth';

export const Library: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<{ userId: string; email: string } | null>(null);

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
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome to your library! 🎉</h2>
            <p className="text-gray-600">You've successfully connected your Spotify account.</p>
            {user && <p className="text-sm text-gray-500 mt-2">User ID: {user.userId}</p>}
          </div>

          {/* Coming Soon */}
          <div className="bg-linear-to-br from-slate-100 to-slate-300 rounded-lg p-8 text-center">
            <div className="text-6xl mb-4">🚧</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Library features coming soon!</h3>
            <p className="text-gray-600 mb-6">
              We're building the library view to show all your tracks. Stay tuned!
            </p>
            <div className="grid md:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="bg-white rounded-lg p-4">
                <div className="text-2xl mb-2">🎵</div>
                <p className="text-sm font-medium">View all tracks</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="text-2xl mb-2">🔍</div>
                <p className="text-sm font-medium">Search & filter</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <div className="text-2xl mb-2">➕</div>
                <p className="text-sm font-medium">Add manually</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
