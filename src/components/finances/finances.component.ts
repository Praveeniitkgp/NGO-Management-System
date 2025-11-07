
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { DataService } from '../../services/data.service';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-finances',
  templateUrl: './finances.component.html',
  imports: [CurrencyPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FinancesComponent {
  private dataService = inject(DataService);

  expenditures = this.dataService.expenditures;
  classNeeds = this.dataService.classNeeds;

  totalExpenditure = computed(() => this.expenditures().reduce((sum, e) => sum + e.amount, 0));
  totalNeeds = computed(() => this.classNeeds().reduce((sum, c) => sum + c.total, 0));
}
