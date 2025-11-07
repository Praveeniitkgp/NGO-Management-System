
import { Injectable, signal } from '@angular/core';

export interface Student {
  id: number;
  name: string;
  age: number;
  class: string;
  performance: 'Excellent' | 'Good' | 'Average' | 'Needs Improvement';
  needs: string[];
  sponsorshipStatus: 'Sponsored' | 'Not Sponsored';
  sponsorId?: number;
}

export interface Donor {
  id: number;
  name: string;
  type: 'Individual' | 'Corporate';
  totalDonated: number;
  lastDonationDate: string;
}

export interface RegisteredDonor {
  id: number;
  name: string;
  email: string;
  mobileNumber: string;
  address: string;
  password_plaintext: string;
}

export interface InventoryItem {
  id: number;
  name: string;
  category: string;
  quantity: number;
  lowStockThreshold: number;
}

export interface Expenditure {
  id: number;
  description: string;
  amount: number;
  date: string;
  category: 'Supplies' | 'Utilities' | 'Staff' | 'Maintenance';
}

export interface ClassNeed {
  id: number;
  class: string;
  item: string;
  quantityNeeded: number;
  costPerItem: number;
  total: number;
}


@Injectable({
  providedIn: 'root',
})
export class DataService {
  students = signal<Student[]>([
    { id: 1, name: 'Alice Smith', age: 8, class: '3rd Grade', performance: 'Excellent', needs: ['Books', 'Uniform'], sponsorshipStatus: 'Sponsored', sponsorId: 1 },
    { id: 2, name: 'Bob Johnson', age: 9, class: '4th Grade', performance: 'Good', needs: ['Stationery'], sponsorshipStatus: 'Not Sponsored' },
    { id: 3, name: 'Charlie Brown', age: 7, class: '2nd Grade', performance: 'Average', needs: ['Lunch Box', 'Shoes'], sponsorshipStatus: 'Not Sponsored' },
    { id: 4, name: 'Diana Prince', age: 10, class: '5th Grade', performance: 'Excellent', needs: [], sponsorshipStatus: 'Sponsored', sponsorId: 2 },
    { id: 5, name: 'Ethan Hunt', age: 8, class: '3rd Grade', performance: 'Needs Improvement', needs: ['Tuition Fee', 'Bag'], sponsorshipStatus: 'Not Sponsored' },
  ]);

  donors = signal<Donor[]>([
    { id: 1, name: 'John Doe', type: 'Individual', totalDonated: 5000, lastDonationDate: '2024-05-15' },
    { id: 2, name: 'Tech Corp', type: 'Corporate', totalDonated: 25000, lastDonationDate: '2024-04-20' },
    { id: 3, name: 'Jane Roe', type: 'Individual', totalDonated: 2500, lastDonationDate: '2024-06-01' },
  ]);

  registeredDonors = signal<RegisteredDonor[]>([
    { id: 1, name: 'John Doe', email: 'john.doe@example.com', mobileNumber: '123-456-7890', address: '123 Main St', password_plaintext: 'password123' },
    { id: 2, name: 'Jane Roe', email: 'jane.roe@example.com', mobileNumber: '098-765-4321', address: '456 Oak Ave', password_plaintext: 'password123' },
  ]);

  inventory = signal<InventoryItem[]>([
    { id: 1, name: 'Notebooks', category: 'Stationery', quantity: 150, lowStockThreshold: 50 },
    { id: 2, name: 'Pencils', category: 'Stationery', quantity: 300, lowStockThreshold: 100 },
    { id: 3, name: 'Textbooks - Grade 3', category: 'Books', quantity: 45, lowStockThreshold: 20 },
    { id: 4, name: 'Chairs', category: 'Furniture', quantity: 100, lowStockThreshold: 10 },
    { id: 5, name: 'First Aid Kits', category: 'Health', quantity: 15, lowStockThreshold: 5 },
  ]);

  expenditures = signal<Expenditure[]>([
    { id: 1, description: 'Electricity Bill - May', amount: 1200, date: '2024-06-05', category: 'Utilities' },
    { id: 2, description: 'Purchase of new textbooks', amount: 3500, date: '2024-05-20', category: 'Supplies' },
    { id: 3, description: 'Janitorial Staff Salary - May', amount: 2800, date: '2024-05-30', category: 'Staff' },
    { id: 4, description: 'Plumbing repairs', amount: 800, date: '2024-06-10', category: 'Maintenance' },
  ]);

  classNeeds = signal<ClassNeed[]>([
    { id: 1, class: '2nd Grade', item: 'Art Supplies', quantityNeeded: 30, costPerItem: 15, total: 450 },
    { id: 2, class: '4th Grade', item: 'Science Kits', quantityNeeded: 25, costPerItem: 50, total: 1250 },
    { id: 3, class: '5th Grade', item: 'New Projector', quantityNeeded: 1, costPerItem: 800, total: 800 },
  ]);
}
