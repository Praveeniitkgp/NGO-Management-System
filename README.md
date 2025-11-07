# NGO Management System

A comprehensive web-based management system for NGOs to manage students, donors, inventory, finances, and donations efficiently.

## 🌐 Live Website

**The application is live and accessible at:** [https://praveenpatel.dev](https://praveenpatel.dev)

## Features

### Admin Dashboard
- **Student Management**: Add, edit, and track student information including performance, sponsorship status, and help provided
- **Donor Management**: View and manage registered donors, record donations, and track donation history
- **Inventory Management**: Track inventory items, monitor stock levels, and set low stock alerts
- **Financial Management**: 
  - Record expenditures by category (Supplies, Utilities, Staff, Maintenance)
  - Manage class needs and calculate costs
  - View available funds and financial summaries
- **Authentication**: Secure login with password recovery via security questions and OTP

### Donor Dashboard
- **Profile Management**: Update personal information and donation preferences
- **Donation Management**: Set desired donation amounts, view donation history, and track total contributions
- **Donation Frequency**: Set up recurring donations (Annual, Half-yearly, or One-time)
- **Authentication**: Secure login with password recovery via security questions and OTP

### Public Features
- **Home Page**: Display organization information and donation options
- **Donor Registration**: Easy registration process for new donors
- **Donation Portal**: Public interface for making donations

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development)
- **Frontend**: Django Templates (HTML/CSS/JavaScript)
- **Email Service**: Gmail SMTP (for OTP and notifications)
- **SMS Service**: Twilio (for SMS OTP)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "NGO Management live_COPY"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`

## Environment Variables (Optional)

For production deployment, set these environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `EMAIL_HOST_USER`: Gmail address for sending emails
- `EMAIL_HOST_PASSWORD`: Gmail app password for email service

## Project Structure

```
NGO Management live_COPY/
├── core/                    # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   ├── gmail_service.py    # Email service
│   └── sms_service.py      # SMS service
├── ngomanagement/          # Django project settings
│   ├── settings.py         # Project configuration
│   └── urls.py             # Main URL configuration
├── static/                # Static files (CSS, images)
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Key Models

- **Admin**: Admin user accounts with security questions
- **Student**: Student information, performance, and sponsorship details
- **RegisteredDonor**: Donor accounts with donation preferences
- **Donor**: Donation history and statistics
- **InventoryItem**: Inventory tracking with low stock alerts
- **Expenditure**: Financial expenditure records
- **ClassNeed**: Class-specific needs and cost calculations

## Usage

### Admin Access
1. Navigate to `/admin-login/`
2. Login with admin credentials
3. Access dashboard at `/admin/dashboard/`

### Donor Access
1. Register at `/register-donor/` or login at `/donor-login/`
2. Access dashboard at `/donor-dashboard/`
3. Update donation preferences and view history

## Security Features

- Session-based authentication
- Password recovery via security questions
- OTP verification via email and SMS
- CSRF protection
- Secure password handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for use.

## Support

For issues and questions, please open an issue in the repository.
