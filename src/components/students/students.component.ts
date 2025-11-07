
import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { DataService, Student } from '../../services/data.service';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  imports: [CurrencyPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StudentsComponent {
  private dataService = inject(DataService);
  students = this.dataService.students;

  getPerformanceClass(performance: Student['performance']): string {
    switch (performance) {
      case 'Excellent': return 'bg-green-100 text-green-800';
      case 'Good': return 'bg-blue-100 text-blue-800';
      case 'Average': return 'bg-yellow-100 text-yellow-800';
      case 'Needs Improvement': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }
}
