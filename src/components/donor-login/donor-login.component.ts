import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DonorAuthService } from '../../services/donor-auth.service';
import { LogoComponent } from '../logo/logo.component';

@Component({
  selector: 'app-donor-login',
  templateUrl: './donor-login.component.html',
  imports: [RouterLink, FormsModule, LogoComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DonorLoginComponent {
  email = signal('');
  password = signal('');
  errorMessage = signal('');
  
  private donorAuthService = inject(DonorAuthService);
  private router = inject(Router);

  currentYear = new Date().getFullYear();

  login(): void {
    if (this.donorAuthService.login(this.email(), this.password())) {
      this.errorMessage.set('');
      this.router.navigate(['/donor-dashboard']);
    } else {
      this.errorMessage.set('Invalid credentials. Please try again.');
    }
  }
}
