import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { SpotifyCallback } from './pages/SpotifyCallback';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/callback/spotify" element={<SpotifyCallback />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
