import { useNavigate } from 'react-router-dom';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleGetStartedButton = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-500 to-slate-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center text-white">
          {/* Hero Section */}
          <h1 className="text-6xl font-bold mb-6">Welcome to Melodiary</h1>
          <p className="text-2xl mb-12 text-white/90">
            Your music library, consolidated across all streaming platforms
          </p>
          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white/10 backdrop-blur-xl rounded-xl p-6">
              <div className="text-4xl mb-4">🎵</div>
              <h3 className="text-xl font-semibold mb-2">Connect Services</h3>
              <p className="text-white/80">Link Spotify, Apple Music, and more in one place</p>
            </div>
            <div className="bg-white/10 backdrop-blur-xl rounded-xl p-6">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-semibold mb-2">Unified Library</h3>
              <p className="text-white/80">See all your music from every platform together</p>
            </div>
            <div className="bg-white/10 backdrop-blur-xl rounded-xl p-6">
              <div className="text-4xl mb-4">🔔</div>
              <h3 className="text-xl font-semibold mb-2">New Releases</h3>
              <p className="text-white/80">
                Get notified when your favorite artists drop new music
              </p>
            </div>
          </div>

          {/* Call to action */}
          <button
            onClick={handleGetStartedButton}
            className="rounded-full bg-sky-500 px-8 py-4 text-lg leading-5 font-semibold text-white hover:bg-sky-600 transition-colors shadow-lg"
            type="button"
          >
            Get Started
          </button>
        </div>
      </div>
    </div>
  );
};
