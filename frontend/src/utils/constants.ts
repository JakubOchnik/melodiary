import type { Platform } from '../types';

export const PLATFORMS: Record<Platform, { name: string; color: string; icon: string }> = {
  spotify: {
    name: 'Spotify',
    color: '#1DB954',
    icon: '🎵',
  },
  manual: {
    name: 'Manual',
    color: '#6B7280',
    icon: '✍️',
  },
};

export const ITEMS_PER_PAGE = 50;

export const SORT_OPTIONS = [
  { value: 'addedDate', label: 'Recently Added' },
  { value: 'trackName', label: 'Track Name' },
  { value: 'artistName', label: 'Artist Name' },
] as const;
