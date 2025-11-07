
import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isAuthenticated = signal<boolean>(false);

  login(password: string): boolean {
    // In a real app, this would be a proper authentication call.
    // Here we use a simple hardcoded password for demonstration.
    if (password === 'admin123') {
      this.isAuthenticated.set(true);
      return true;
    }
    return false;
  }

  logout(): void {
    this.isAuthenticated.set(false);
  }
}
