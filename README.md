# NGO Management System

A comprehensive web-based management system for NGOs to manage students, donors, inventory, finances, and donations efficiently.

## Live Website

**The application is live and accessible at:** [https://praveenpatel.dev](https://praveenpatel.dev)

## Features

### Admin Dashboard
- Student Management
- Donor Management
- Inventory Management
- Financial Management
- Secure authentication with password recovery

### Donor Dashboard
- Profile Management
- Donation Management
- View donation history
- Secure authentication with password recovery

### Public Features
- Home Page
- Donor Registration
- Donation Portal

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates with Tailwind CSS
- **Email Service**: Gmail API
- **SMS Service**: Twilio

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Praveeniitkgp/NGO-Management-System.git
   cd NGO-Management-System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run server**
   ```bash
   python manage.py runserver
   ```

7. **Access application**
   - Open browser and navigate to `http://localhost:8000`

## Security Features

- Password hashing using Django's PBKDF2 algorithm
- CSRF protection
- SQL injection protection
- Security headers enabled in production
- SSL/HTTPS support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for use.

---

**Live Demo**: [https://praveenpatel.dev](https://praveenpatel.dev)

