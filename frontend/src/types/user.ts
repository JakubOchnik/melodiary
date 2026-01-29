import type { Platform } from './track';

export interface User {
  userId: string;
  email: string;
  displayName: string;
  createdAt: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  emailNotifications: boolean;
  notificationFrequency: 'daily' | 'weekly' | 'never';
  emailAddress?: string;
  theme?: 'light' | 'dark' | 'auto';
}

export interface PlatformConnection {
  userId: string;
  platform: Platform;
  connected: boolean;
  connectedAt?: string;
  displayName?: string;
  profileUrl?: string;
}

export interface UserStats {
  totalTracks: number;
  totalArtists: number;
  platformBreakdown: {
    platform: Platform;
    count: number;
  }[];
  recentlyAdded: number;
}
