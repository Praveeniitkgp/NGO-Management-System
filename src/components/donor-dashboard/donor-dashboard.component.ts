
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CurrencyPipe } from '@angular/common';
import { DonorAuthService } from '../../services/donor-auth.service';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-donor-dashboard',
  imports: [RouterLink, CurrencyPipe],
  template: `
    <div class="min-h-screen bg-gray-50">
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">
            Welcome, {{ donorName() }}
          </h1>
          <button (click)="logout()" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Logout
          </button>
        </div>
      </header>
      
      <main class="py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Donor Profile -->
            <div class="md:col-span-1 bg-white rounded-lg shadow-md p-6">
              <h2 class="text-lg font-semibold text-gray-800 mb-4">Your Profile</h2>
              @if(currentDonor(); as donor) {
                <div class="space-y-3 text-sm text-gray-600">
                  <p><span class="font-medium text-gray-900">Name:</span> {{ donor.name }}</p>
                  <p><span class="font-medium text-gray-900">Email:</span> {{ donor.email }}</p>
                  <p><span class="font-medium text-gray-900">Mobile:</span> {{ donor.mobileNumber }}</p>
                  <p><span class="font-medium text-gray-900">Address:</span> {{ donor.address }}</p>
                </div>
              }
            </div>

            <!-- Donation Opportunities -->
            <div class="md:col-span-2 bg-white rounded-lg shadow-md p-6">
              <h2 class="text-lg font-semibold text-gray-800 mb-4">How You Can Help</h2>
              <p class="text-sm text-gray-600 mb-6">Here are some of the current needs at our school. Your support can make a huge difference!</p>
              
              <div class="overflow-x-auto">
                <table class="w-full text-sm text-left text-gray-500">
                  <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3">Class</th>
                      <th scope="col" class="px-6 py-3">Item Needed</th>
                      <th scope="col" class="px-6 py-3">Total Cost</th>
                    </tr>
                  </thead>
                  <tbody>
                    @for(need of classNeeds(); track need.id) {
                      <tr class="bg-white border-b hover:bg-gray-50">
                        <td class="px-6 py-4 font-medium text-gray-900">{{ need.class }}</td>
                        <td class="px-6 py-4">{{ need.item }} ({{ need.quantityNeeded }} units)</td>
                        <td class="px-6 py-4 font-semibold text-blue-600">{{ need.total | currency:'USD' }}</td>
                      </tr>
                    }
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          
          <div class="mt-8 bg-white rounded-lg shadow-md p-6">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">Students You've Sponsored</h2>
             @if (sponsoredStudents().length > 0) {
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                @for(student of sponsoredStudents(); track student.id) {
                   <div class="border rounded-lg p-4 flex items-center space-x-4">
                     <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xl">
                       {{ student.name.charAt(0) }}
                     </div>
                     <div>
                       <p class="font-semibold text-gray-800">{{ student.name }}</p>
                       <p class="text-sm text-gray-500">{{ student.class }}</p>
                     </div>
                   </div>
                }
              </div>
            } @else {
              <p class="text-gray-500 italic">You have not sponsored any students yet.</p>
            }
          </div>

        </div>
      </main>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DonorDashboardComponent {
  private donorAuthService = inject(DonorAuthService);
  private dataService = inject(DataService);
  private router = inject(Router);

  currentDonor = this.donorAuthService.currentDonor;
  donorName = computed(() => this.currentDonor()?.name || 'Donor');

  classNeeds = this.dataService.classNeeds;
  
  sponsoredStudents = computed(() => {
    const donorId = this.currentDonor()?.id;
    if (!donorId) return [];
    return this.dataService.students().filter(s => s.sponsorId === donorId);
  });

  logout(): void {
    this.donorAuthService.logout();
    this.router.navigate(['/donor-login']);
  }
}
