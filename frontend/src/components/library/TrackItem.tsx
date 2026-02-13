import type { Track } from '../../types';

interface TrackItemProps {
  track: Track;
}

export const TrackItem: React.FC<TrackItemProps> = ({ track }) => {
  return (
    <li className="flex items-center gap-4 p-4 hover:bg-gray-50">
      {track.coverArtUrl ? (
        <img
          src={track.coverArtUrl}
          alt={track.albumName}
          className="w-12 h-12 rounded object-cover flex-shrink-0"
        />
      ) : (
        <div className="w-12 h-12 rounded bg-gray-200 flex items-center justify-center flex-shrink-0">
          <span className="text-gray-400 text-xs">N/A</span>
        </div>
      )}
      <div className="min-w-0 flex-1">
        <p className="font-medium text-gray-900 truncate">{track.trackName}</p>
        <p className="text-sm text-gray-500 truncate">
          {track.artistName} &middot; {track.albumName}
        </p>
      </div>
      <span className="text-xs text-gray-400 flex-shrink-0">{track.platform}</span>
    </li>
  );
};
