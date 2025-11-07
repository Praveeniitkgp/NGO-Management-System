import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { DataService, RegisteredDonor } from '../../services/data.service';
import { CurrencyPipe } from '@angular/common';
import { LogoComponent } from '../logo/logo.component';

@Component({
  selector: 'app-donor-registration',
  imports: [RouterLink, ReactiveFormsModule, CurrencyPipe, LogoComponent],
  templateUrl: './donor-registration.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DonorRegistrationComponent {
    private fb = inject(FormBuilder);
    private dataService = inject(DataService);
    private router = inject(Router);

    submissionMessage = signal('');

    registrationForm: FormGroup;
    currentYear = new Date().getFullYear();

    constructor() {
        this.registrationForm = this.fb.group({
            name: ['', Validators.required],
            email: ['', [Validators.required, Validators.email]],
            mobileNumber: ['', Validators.required],
            address: ['', Validators.required],
            password: ['', [Validators.required, Validators.minLength(6)]]
        });
    }

    onSubmit(): void {
        if (this.registrationForm.valid) {
            const newDonor: Omit<RegisteredDonor, 'id'> = {
                name: this.registrationForm.value.name!,
                email: this.registrationForm.value.email!,
                mobileNumber: this.registrationForm.value.mobileNumber!,
                address: this.registrationForm.value.address!,
                password_plaintext: this.registrationForm.value.password!
            };

            this.dataService.registeredDonors.update(donors => [
                ...donors,
                {
                    ...newDonor,
                    id: donors.length + 1,
                }
            ]);

            this.submissionMessage.set('Thank you for registering! You will be redirected to the login page shortly.');
            this.registrationForm.reset();

            setTimeout(() => this.router.navigate(['/donor-login']), 3000);
        }
    }
}
