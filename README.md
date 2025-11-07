# NGO Management System

A comprehensive web-based management system for NGOs to efficiently manage students, donors, inventory, finances, and donations.

## 🌐 Live Website

**The application is live and accessible at:** [https://praveenpatel.dev](https://praveenpatel.dev)

## ✨ Features

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

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates with Tailwind CSS
- **Email Service**: Gmail API (for OTP and notifications)
- **SMS Service**: Twilio (for SMS OTP)
- **Deployment**: Nginx + Gunicorn
- **SSL**: Let's Encrypt (HTTPS)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Praveeniitkgp/NGO-Management-System.git
   cd NGO-Management-System
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

4. **Configure environment variables**
   ```bash
   ./setup_env.sh
   ```
   Or manually create a `.env` file with:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create admin account** (optional)
   ```bash
   python manage.py shell
   >>> from core.models import Admin
   >>> admin = Admin(email='admin@example.com', name='Admin')
   >>> admin.set_password('YourSecurePassword123!')
   >>> admin.save()
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`

## 📁 Project Structure

```
NGO-Management-System/
├── core/                    # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   ├── gmail_service.py    # Email service
│   └── sms_service.py      # SMS service
├── ngomanagement/          # Django project settings
│   ├── settings.py        # Project configuration
│   └── urls.py             # Main URL configuration
├── static/                 # Static files (CSS, images)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── auto_deploy.sh          # Automated deployment script
├── deploy_to_server.sh      # Server deployment script
└── server_setup.sh         # Initial server setup script
```

## 🔐 Security Features

- **Password Hashing**: All passwords are securely hashed using Django's PBKDF2 algorithm
- **CSRF Protection**: Enabled by default
- **Session Security**: Secure session cookies in production
- **SQL Injection Protection**: Parameterized queries used throughout
- **Security Headers**: HSTS, XSS protection, and content type sniffing protection enabled in production
- **SSL/HTTPS**: SSL certificate configuration included for production

## 📊 Database Models

- **Admin**: Admin user accounts with security questions
- **Student**: Student information, performance, and sponsorship details
- **RegisteredDonor**: Donor accounts with donation preferences
- **Donor**: Donation history and statistics
- **InventoryItem**: Inventory tracking with low stock alerts
- **Expenditure**: Financial expenditure records
- **ClassNeed**: Class-specific needs and cost calculations

## 🌍 Production Deployment

### 1. Configure Environment Variables

```bash
./setup_env.sh
```

### 2. Deploy to Server

```bash
./auto_deploy.sh
```

This will:
- Upload code to server
- Install dependencies
- Run migrations
- Hash existing passwords
- Collect static files
- Restart services

### 3. Configure SSL Certificate

On your production server:

```bash
sudo ./configure_ssl.sh
```

## 📝 Environment Variables

For production deployment, configure these in your `.env` file:

```env
# Production Settings
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=praveenpatel.dev,www.praveenpatel.dev,your-server-ip

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Admin Credentials (optional, for auto-deployment)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=YourSecurePassword123!
ADMIN_SECURITY_ANSWER=your-answer
```

**Important**: 
- Generate SECRET_KEY using: `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Never commit `.env` file to version control
- Use strong, unique SECRET_KEY in production

## 🧪 Testing

Run the security test suite:

```bash
python test_security.py
```

This tests:
- Password hashing
- Login functionality
- Password reset functionality
- Environment variable configuration

## 📖 Usage

### Admin Access
1. Navigate to `/admin-login/`
2. Login with admin credentials
3. Access dashboard at `/admin/dashboard/`

### Donor Access
1. Register at `/register-donor/` or login at `/donor-login/`
2. Access dashboard at `/donor-dashboard/`
3. Update donation preferences and view history

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for use.

## 🐛 Issues

If you encounter any issues or have questions, please open an issue in the repository.

## 👤 Author

**Praveen Kumar**
- GitHub: [@Praveeniitkgp](https://github.com/Praveeniitkgp)
- Website: [praveenpatel.dev](https://praveenpatel.dev)

## 🙏 Acknowledgments

- Django Framework
- Tailwind CSS
- Twilio for SMS services
- Gmail API for email services

---

**Live Demo**: [https://praveenpatel.dev](https://praveenpatel.dev)
