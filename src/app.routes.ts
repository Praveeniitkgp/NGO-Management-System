import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { donorAuthGuard } from './guards/donor-auth.guard';

export const APP_ROUTES: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./components/home/home.component').then(c => c.HomeComponent)
  },
  {
    path: 'admin-login',
    loadComponent: () => import('./components/admin-login/admin-login.component').then(c => c.AdminLoginComponent)
  },
  {
    path: 'register-donor',
    loadComponent: () => import('./components/donor-registration/donor-registration.component').then(c => c.DonorRegistrationComponent)
  },
  {
    path: 'donor-login',
    loadComponent: () => import('./components/donor-login/donor-login.component').then(c => c.DonorLoginComponent)
  },
  {
    path: 'donor-dashboard',
    loadComponent: () => import('./components/donor-dashboard/donor-dashboard.component').then(c => c.DonorDashboardComponent),
    canActivate: [donorAuthGuard]
  },
  {
    path: 'admin',
    loadComponent: () => import('./components/admin-layout/admin-layout.component').then(c => c.AdminLayoutComponent),
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      {
        path: 'dashboard',
        loadComponent: () => import('./components/dashboard/dashboard.component').then(c => c.DashboardComponent)
      },
      {
        path: 'students',
        loadComponent: () => import('./components/students/students.component').then(c => c.StudentsComponent)
      },
      {
        path: 'donors',
        loadComponent: () => import('./components/donors/donors.component').then(c => c.DonorsComponent)
      },
      {
        path: 'inventory',
        loadComponent: () => import('./components/inventory/inventory.component').then(c => c.InventoryComponent)
      },
      {
        path: 'finances',
        loadComponent: () => import('./components/finances/finances.component').then(c => c.FinancesComponent)
      },
    ]
  },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', redirectTo: 'home' }
];
