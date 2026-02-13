import axios, { type AxiosInstance, AxiosError } from 'axios';

import type {
  Track,
  User,
  PlatformConnection,
  ApiError,
  PaginatedResponse,
  SpotifyAuthUrlResponse,
  AuthCallbackResponse,
  LibraryQueryParams,
  Playlist,
  UserPreferences,
  SyncPlatformResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('melodiary_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        // Invalid or expired token
        if (error.response?.status === 401) {
          localStorage.removeItem('melodiary_token');
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  auth = {
    getSpotifyAuthUrl: async (): Promise<string> => {
      const response = await this.client.get<SpotifyAuthUrlResponse>('/auth/spotify/login');
      return response.data.authUrl;
    },

    spotifyCallback: async (code: string): Promise<AuthCallbackResponse> => {
      const response = await this.client.post<AuthCallbackResponse>('/auth/spotify/callback', {
        code,
      });
      return response.data;
    },

    logout: (): void => {
      localStorage.removeItem('melodiary_token');
      window.location.href = '/login';
    },
  };

  library = {
    getLibrary: async (params?: LibraryQueryParams): Promise<PaginatedResponse<Track>> => {
      const response = await this.client.get<PaginatedResponse<Track>>('/library', {
        params,
      });
      return response.data;
    },

    addManualTrack: async (
      track: Omit<Track, 'trackId' | 'platform' | 'addedDate' | 'isManual'>
    ): Promise<Track> => {
      const response = await this.client.post<Track>('/library/manual', track);
      return response.data;
    },

    deleteTrack: async (trackId: string): Promise<void> => {
      await this.client.delete(`/library/${encodeURIComponent(trackId)}`);
    },

    syncPlatform: async (platform: string): Promise<SyncPlatformResponse> => {
      const response = await this.client.post<SyncPlatformResponse>(`/library/sync/${platform}`);
      return response.data;
    },
  };

  user = {
    getProfile: async (): Promise<User> => {
      const response = await this.client.get<User>('/user/profile');
      return response.data;
    },

    updatePreferences: async (preferences: Partial<UserPreferences>): Promise<User> => {
      const response = await this.client.put<User>('/user/preferences', preferences);
      return response.data;
    },

    getPlatformConnections: async (): Promise<PlatformConnection[]> => {
      const response = await this.client.get<PlatformConnection[]>('/user/connections');
      return response.data;
    },

    disconnectPlatform: async (platform: string): Promise<void> => {
      await this.client.delete(`/user/connections/${platform}`);
    },
  };

  playlists = {
    getPlaylists: async (platform: string): Promise<Playlist[]> => {
      const response = await this.client.get<Playlist[]>(`/playlists/${platform}`);
      return response.data;
    },

    exportPlaylist: async (platform: string, playlistId: string): Promise<Track[]> => {
      const response = await this.client.get<Track[]>(
        `/playlists/${platform}/${playlistId}/export`
      );
      return response.data;
    },

    importPlaylist: async (
      targetPlatform: string,
      playlistName: string,
      tracks: Track[]
    ): Promise<{ success: number; failed: number; playlistUrl: string }> => {
      const response = await this.client.post(`/playlists/${targetPlatform}/import`, {
        playlistName,
        tracks,
      });
      return response.data;
    },
  };
}

const api = new ApiService();
export default api;
