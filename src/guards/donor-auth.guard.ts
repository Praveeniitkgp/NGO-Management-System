import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { DonorAuthService } from '../services/donor-auth.service';

export const donorAuthGuard: CanActivateFn = () => {
  const donorAuthService = inject(DonorAuthService);
  const router = inject(Router);

  if (donorAuthService.isAuthenticated()) {
    return true;
  } else {
    router.navigate(['/donor-login']);
    return false;
  }
};
