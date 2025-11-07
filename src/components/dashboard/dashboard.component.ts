
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { DataService } from '../../services/data.service';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe],
  template: `
    <div class="p-4 sm:p-6 md:p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Admin Dashboard</h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Total Students -->
        <div class="bg-white rounded-lg shadow-md p-6 flex flex-col justify-between">
          <div>
            <h2 class="text-sm font-medium text-gray-500">Total Students</h2>
            <p class="text-3xl font-bold text-gray-900">{{ totalStudents() }}</p>
          </div>
          <div class="mt-4">
            <p class="text-sm text-green-600">{{ sponsoredStudents() }} Sponsored</p>
            <p class="text-sm text-yellow-600">{{ unsponsoredStudents() }} Need Sponsorship</p>
          </div>
        </div>

        <!-- Total Donors -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-sm font-medium text-gray-500">Total Donors</h2>
          <p class="text-3xl font-bold text-gray-900">{{ totalDonors() }}</p>
        </div>

        <!-- Total Donations -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-sm font-medium text-gray-500">Total Donations</h2>
          <p class="text-3xl font-bold text-gray-900">{{ totalDonations() | currency:'USD':'symbol':'1.0-0' }}</p>
        </div>

        <!-- Inventory Status -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-sm font-medium text-gray-500">Inventory Status</h2>
          <p class="text-3xl font-bold text-gray-900">{{ lowStockItems() }}</p>
          <p class="text-sm text-gray-500 mt-1">items running low</p>
        </div>
      </div>

      <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Expenditures -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Recent Expenditures</h3>
          <ul class="space-y-3">
            @for (item of recentExpenditures(); track item.id) {
              <li class="flex justify-between items-center">
                <div>
                  <p class="font-medium text-gray-700">{{ item.description }}</p>
                  <p class="text-sm text-gray-500">{{ item.date }} - {{ item.category }}</p>
                </div>
                <p class="font-semibold text-red-600">{{ item.amount | currency:'USD' }}</p>
              </li>
            }
          </ul>
        </div>
        
        <!-- Urgent Class Needs -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Urgent Class Needs</h3>
          <ul class="space-y-3">
            @for (item of classNeeds(); track item.id) {
              <li class="flex justify-between items-center">
                <div>
                  <p class="font-medium text-gray-700">{{ item.item }} ({{ item.class }})</p>
                  <p class="text-sm text-gray-500">{{ item.quantityNeeded }} units needed</p>
                </div>
                <p class="font-semibold text-blue-600">{{ item.total | currency:'USD' }}</p>
              </li>
            }
          </ul>
        </div>
      </div>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent {
  private dataService = inject(DataService);

  totalStudents = computed(() => this.dataService.students().length);
  sponsoredStudents = computed(() => this.dataService.students().filter(s => s.sponsorshipStatus === 'Sponsored').length);
  unsponsoredStudents = computed(() => this.totalStudents() - this.sponsoredStudents());
  
  totalDonors = computed(() => this.dataService.donors().length);
  totalDonations = computed(() => this.dataService.donors().reduce((acc, donor) => acc + donor.totalDonated, 0));
  
  lowStockItems = computed(() => this.dataService.inventory().filter(item => item.quantity <= item.lowStockThreshold).length);

  recentExpenditures = computed(() => this.dataService.expenditures().slice(0, 5));
  classNeeds = this.dataService.classNeeds;
}
