
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { DataService } from '../../services/data.service';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-donors',
  imports: [CurrencyPipe],
  template: `
    <div class="p-4 sm:p-6 md:p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Donors</h1>
      
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3">Donor Name</th>
                <th scope="col" class="px-6 py-3">Type</th>
                <th scope="col" class="px-6 py-3">Total Donated</th>
                <th scope="col" class="px-6 py-3">Last Donation</th>
              </tr>
            </thead>
            <tbody>
              @for (donor of donors(); track donor.id) {
                <tr class="bg-white border-b hover:bg-gray-50">
                  <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                    {{ donor.name }}
                  </th>
                  <td class="px-6 py-4">
                    <span 
                      class="px-2 py-1 text-xs font-medium rounded-full"
                      [class]="donor.type === 'Corporate' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
                      {{ donor.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4">{{ donor.totalDonated | currency:'USD':'symbol':'1.0-0' }}</td>
                  <td class="px-6 py-4">{{ donor.lastDonationDate }}</td>
                </tr>
              }
            </tbody>
            <tfoot>
              <tr class="font-semibold text-gray-900 bg-gray-50">
                <th scope="row" colspan="2" class="px-6 py-3 text-base text-right">Total</th>
                <td class="px-6 py-3 text-base">{{ totalDonations() | currency:'USD':'symbol':'1.0-0' }}</td>
                <td class="px-6 py-3"></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DonorsComponent {
  private dataService = inject(DataService);
  donors = this.dataService.donors;
  
  totalDonations = computed(() => this.donors().reduce((sum, d) => sum + d.totalDonated, 0));
}
