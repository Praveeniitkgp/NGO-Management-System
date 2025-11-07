
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-admin-login',
  templateUrl: './admin-login.component.html',
  imports: [RouterLink, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AdminLoginComponent {
  password = signal('');
  errorMessage = signal('');
  
  private authService = inject(AuthService);
  private router = inject(Router);

  login(): void {
    if (this.authService.login(this.password())) {
      this.errorMessage.set('');
      this.router.navigate(['/admin']);
    } else {
      this.errorMessage.set('Invalid credentials. Please try again.');
    }
  }
}
