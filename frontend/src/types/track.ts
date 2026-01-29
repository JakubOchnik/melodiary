export type Platform = 'spotify' | 'manual'; // TODO: add more platforms in the future

export interface Track {
  trackId: string;
  trackName: string;
  artistName: string;
  albumName: string;
  platform: Platform;
  platformTrackId?: string;
  platformAlbumId?: string;
  platformArtistId?: string;
  coverArtUrl?: string;
  addedDate: string;
  isManual: boolean;
  duration?: number;
  releaseYear?: number;
  genre?: string;
  notes?: string;
}

export interface Artist {
  artistName: string;
  platforms: Platform[];
  trackCount: number;
  platformArtistIds: {
    spotify?: string; // todo: add more platforms in the future
  };
}

export interface Album {
  albumName: string;
  artistName: string;
  releaseDate?: string;
  coverArtUrl?: string;
  trackCount: number;
  platform: Platform;
}

export interface Playlist {
  playlistId: string;
  name: string;
  platform: Platform;
  trackCount: number;
  description?: string;
  coverArtUrl?: string;
}
