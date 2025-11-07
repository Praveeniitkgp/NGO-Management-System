import { Injectable, signal, inject } from '@angular/core';
import { DataService, RegisteredDonor } from './data.service';

@Injectable({
  providedIn: 'root',
})
export class DonorAuthService {
  private dataService = inject(DataService);

  isAuthenticated = signal<boolean>(false);
  currentDonor = signal<RegisteredDonor | null>(null);

  login(email: string, password_plaintext: string): boolean {
    const donor = this.dataService.registeredDonors().find(
        d => d.email === email && d.password_plaintext === password_plaintext
    );

    if (donor) {
      this.isAuthenticated.set(true);
      this.currentDonor.set(donor);
      return true;
    }
    return false;
  }

  logout(): void {
    this.isAuthenticated.set(false);
    this.currentDonor.set(null);
  }
}
