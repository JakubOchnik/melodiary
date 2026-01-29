import api from './api';

export interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  userId: string | null;
}

class AuthManager {
  private readonly TOKEN_KEY = 'melodiary_token';
  private readonly USER_ID_KEY = 'melodiary_user_id';

  getAuthState(): AuthState {
    const token = localStorage.getItem(this.TOKEN_KEY);
    const userId = localStorage.getItem(this.USER_ID_KEY);
    return {
      isAuthenticated: !!token,
      token,
      userId,
    };
  }

  setAuth(token: string, userId: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    localStorage.setItem(this.USER_ID_KEY, userId);
  }

  clearAuth(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_ID_KEY);
  }

  async logout(): Promise<void> {
    this.clearAuth();
    api.auth.logout();
  }

  isTokenExpired(): boolean {
    // TODO JWT decode
    return false;
  }
}

export const authManager = new AuthManager();
