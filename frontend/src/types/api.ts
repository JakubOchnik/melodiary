export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  count: number;
  lastKey: Record<string, string> | null;
}

export interface SpotifyAuthUrlResponse {
  authUrl: string;
}

export interface AuthCallbackResponse {
  token: string;
  user: {
    userId: string;
    email: string;
    displayName: string;
  };
}

export interface LibraryQueryParams {
  limit?: number;
  lastKey?: string;
}

export interface SyncPlatformResponse {
  synced: number;
  malformed: number;
  message: string;
}
