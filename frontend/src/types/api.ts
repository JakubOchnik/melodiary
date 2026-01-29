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
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
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
  page?: number;
  pageSize?: number;
  platform?: string;
  search?: string;
  sortBy?: 'addedDate' | 'trackName' | 'artistName';
  sortOrder?: 'asc' | 'desc';
}
