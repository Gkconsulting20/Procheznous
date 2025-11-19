# PRO CHEZ NOUS

## Overview
PRO CHEZ NOUS is a French professional appointment booking platform designed for manual trades (métiers manuels). It connects clients with skilled tradespeople, enabling them to find, book, and manage appointments based on location, professional category, ratings, and availability. The platform aims to streamline the booking process for both clients and professionals, offering a freemium model with enhanced features for premium subscribers.

**Pricing:** 1000 FCFA/month for Premium plan (Prix de lancement)
**Payment Methods:** T-Money (Togocel) and Flooz (Moov Africa)
**Target Market:** West Africa (Togo, Benin, Burkina Faso, etc.)
**Deployment:** PythonAnywhere (SQLite persistent, plan gratuit disponible)

## User Preferences
- Language: French (application interface)
- Database: SQLite (existing choice maintained)
- Authentication: Email OR phone number (to accommodate African market where phone numbers are more common)

## System Architecture

### Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML templates with Jinja2, Custom CSS
- **Deployment**: Configured for Replit autoscale deployment, designed for production with Gunicorn.

### Core Design Decisions
- **UI/UX**: Modern, responsive design with a RED theme, card-based layouts, and custom logos. Features intuitive dashboards for both clients and professionals.
- **Security**: Robust security measures including bcrypt password hashing, environment variable for secret key, comprehensive form validation, and **role-based access control (RBAC)** with three distinct roles: 'user' (client), 'pro' (professional), and 'admin' (administrator). Admin panel is strictly restricted to users with 'admin' role.
- **Freemium Model**: Implements a "gratuit" and "premium" subscription system (1000 FCFA/month - prix de lancement), gating advanced features like internal messaging, favorites, enriched profiles, advanced statistics, and geolocation. Payment via T-Money or Flooz.
- **Geolocation**: Premium-only feature utilizing HTML5 Geolocation API, Haversine formula for distance calculation, and sorting professionals by proximity.
- **Professional Verification**: System for professionals to upload verification documents, with statuses and a "✓ Vérifié" badge for verified profiles.
- **Scalability**: Designed with a clear project structure and plans for production-grade WSGI server (Gunicorn).

### Feature Specifications
- **User Management**: Secure registration and authentication for both clients and professionals using **email OR phone number**. Password recovery with secure token-based system (1-hour expiration) supporting both email and phone number. **Admin accounts** can be created using `create_admin.py` script with full platform management privileges.
- **Admin Panel (Admin-only)**: Accessible only to users with 'admin' role. Features include:
  - Document verification management for professional accounts
  - **Category Management**: Full CRUD interface to create, edit, activate/deactivate, and delete professional trade categories. Displays usage statistics (number of professionals per category) and prevents deletion of categories in use.
- **Professional Discovery**: Browsing, advanced search, and filtering by name, city, category, and minimum rating. Professionals are sorted by rating by default, and by proximity for premium users.
- **Appointment Management**: Professionals manage time slots, clients book and cancel appointments, with automatic slot restoration.
- **Rating System**: Clients can rate and review professionals.
- **Dashboards**: Interactive dashboards for both user types displaying appointments, statistics (for premium professionals), and quick actions.
- **Internal Messaging (Premium)**: Private communication between clients and professionals.
- **Favorites System (Premium)**: Clients can save preferred professionals.
- **Enriched Professional Profiles (Premium)**: Detailed profiles with descriptions, rates, experience, certifications, and photo galleries.
- **Advanced Statistics (Premium)**: For professionals, includes profile views, booking analytics, and revenue tracking.
- **Subscription Management**: Easy upgrade path to premium.
- **Password Recovery**: Users can reset forgotten passwords via secure token system (demo version displays link directly, production ready for email integration).

### Database Schema Highlights
- `users`: Stores user data including email OR phone number (flexible authentication), role, location, plan, verification status, GPS coordinates, commercial_id (tracks which sales rep referred the user), and code_commercial (unique referral code for sales reps).
- `slots`, `rendezvous`: Manages available and booked appointments.
- `avis`: Stores client ratings and reviews.
- `profils_pro`: Extends professional profiles for premium users.
- `messages`, `favoris`: Supports premium messaging and favorites features.
- `documents_verification`: Manages professional verification documents.
- `password_reset_tokens`: Manages password reset requests with secure tokens and 1-hour expiration.
- `categories`: Stores professional trade categories with icon, active status, and display order. Managed dynamically via admin panel.

### Professional Categories
The platform features a **dynamic category management system**. Administrators can create, modify, activate/deactivate, and delete professional trade categories through the admin panel. Categories include display order, emoji icons, and usage tracking (number of professionals per category). The system starts with 75 default categories covering manual trades (Plomberie, Électricité, Peinture, Menuiserie, Rénovation, Jardinage, etc.).

## External Dependencies
- **Flask**: Main web framework.
- **SQLite**: Database system.
- **Jinja2**: Templating engine.
- **Bcrypt**: For password hashing.
- **HTML5 Geolocation API**: Used for the premium geolocation feature.
- **FedaPay API**: Payment processing for T-Money, Flooz, and mobile money (optional).
- **SendGrid API**: Email delivery service for password reset and notifications (optional).
- **Twilio API**: SMS service for phone verification (optional).
- **Requests**: HTTP library for API integrations.

## Recent Changes (November 19, 2025)

### Sales Representative (Commercial) Tracking System
- **Status**: ✅ Implemented & Tested
- **Change**: Complete tracking system for sales representatives with referral codes and performance metrics
- **Files**: `app.py`, `create_commercial.py`, `templates/dashboard_commercial.html`, `templates/admin_commerciaux.html`, `templates/base.html`, `templates/register.html`
- **Features**:
  - Database columns: `commercial_id` (INTEGER), `code_commercial` (TEXT with unique index)
  - Script `create_commercial.py` to create commercial accounts with auto-generated 8-character referral codes
  - Unique referral links: `/register?ref=CODE12345` automatically tracks signups to commercial
  - Commercial dashboard showing: total signups, clients vs pros breakdown, premium conversions, revenue tracking
  - Admin panel page `/admin/commerciaux` with global statistics and performance table for all sales reps
  - Referral code normalization (.upper()) to handle case-insensitive URL parameters
- **Security**: Commercial role verification, admin-only access to global reports
- **Migration**: Safe deployment approach using ALTER TABLE + CREATE UNIQUE INDEX (compatible with PythonAnywhere)
- **Usage**: Run `python create_commercial.py` to create sales representative accounts

## Recent Changes (November 01, 2025)

### Migration Testing & Validation
- **Status**: ✅ Tested & Ready for PythonAnywhere
- **Change**: Complete migration testing workflow created and validated
- **Files**: `MIGRATION_COMPLETE_PYTHONANYWHERE.sh`, `DEPLOIEMENT_FINAL_PYTHONANYWHERE.md`, `RESUME_FINAL.md`
- **Tests**:
  - Created "old database" matching PythonAnywhere state (without new columns)
  - Applied migration adding 5 columns: `phone`, `plan`, `statut_verification`, `latitude`, `longitude`
  - Created `categories` table with 75 professional categories
  - Fixed critical bug: column naming inconsistency (`verification_status` → `statut_verification`)
  - Validated all pages load correctly: `/`, `/register`, `/professionals`, `/login`
- **Result**: Migration script validated and ready for production deployment
- **Deployment Guide**: See `DEPLOIEMENT_FINAL_PYTHONANYWHERE.md` for complete step-by-step instructions

### Dynamic Category Management System
- **Status**: ✅ Implemented & Tested
- **Change**: Migrated hardcoded professional categories to database with full admin management interface
- **Files**: `app.py` (lines 32-36, 792-905), `templates/admin_categories.html`, `templates/admin_category_form.html`, `templates/base.html` (lines 43-51)
- **Features**:
  - Database table `categories` with fields: id, nom, icone, actif, ordre, date_creation
  - Admin routes: list, add, edit, delete, toggle active status
  - Helper function `get_categories()` returns active categories ordered by display order
  - Admin UI shows usage statistics (number of professionals per category)
  - Prevents deletion of categories currently in use
  - All registration and professional listing flows use dynamic categories
  - Admin menu includes dropdown with "Vérifications" and "Catégories" options
- **Security**: Admin-only access with role verification on all routes
- **Migration**: 75 default categories automatically seeded on first launch

## Recent Changes (October 31, 2025)

### Security Enhancement - Role-Based Access Control (RBAC)
- **Status**: ✅ Implemented & Deployed
- **Change**: Complete implementation of role-based and plan-based access control
- **Files**: `app.py` (line 126), `templates/base.html` (lines 26-38)
- **Details**: 
  - Session now includes `plan` attribute (added during login)
  - Admin panel visible ONLY to users with `role='admin'`
  - Messages & Favoris tabs visible ONLY to users with `plan='premium'`
  - Routes already protected with server-side checks
  - Session invalidation required after deployment to apply changes
- **Deployment**: Successfully deployed to PythonAnywhere (www.pro-chez-nous.com)
- **Usage**: Run `python create_admin.py` to create admin accounts

## Recent Integrations (October 2024)

### Phone Number Normalization
- **Status**: ✅ Active
- **Features**: Automatic normalization to international format (+XXX)
- **Coverage**: 10 West African countries (Togo, Bénin, Burkina Faso, etc.)
- **Files**: `utils.py`

### FedaPay Payment Integration
- **Status**: ✅ Configuré (clés API ajoutées - novembre 2025)
- **Purpose**: Accept Premium subscription payments (1000 FCFA/month - prix de lancement)
- **Payment Methods**: T-Money, Flooz, MTN Mobile Money, Orange Money, cards
- **Mode**: Sandbox (test) and Live (production) support
- **Files**: `fedapay_service.py`, `templates/upgrade_premium.html`, `templates/payment_redirect.html`, `templates/admin_fedapay_test.html`
- **Configuration**: Set `FEDAPAY_SECRET_KEY`, `FEDAPAY_PUBLIC_KEY`, `FEDAPAY_ENV` in environment
- **Admin Panel**: Page de diagnostic et test disponible à `/admin/fedapay` (menu Admin → FedaPay)
- **Features**:
  - Test de connexion API avec détection d'erreurs
  - Affichage configuration actuelle (environnement, clés, URLs)
  - Guide intégré pour configuration FedaPay
  - Solutions aux erreurs communes (authentification, clés invalides)
- **Sécurité**: Clés stockées dans Replit Secrets, jamais affichées en clair

### SendGrid Email Integration
- **Status**: 🔧 Configured (requires API key)
- **Purpose**: Automated password reset emails
- **Features**: HTML email templates, branded design
- **Files**: `email_service.py`
- **Configuration**: Set `SENDGRID_API_KEY`, `FROM_EMAIL`, `FROM_NAME` in environment
- **Fallback**: If not configured, reset links display on screen (demo mode)

### Twilio SMS Integration
- **Status**: 🔧 Configured (requires credentials)
- **Purpose**: Phone number verification via SMS codes
- **Features**: 6-digit code generation, 10-minute expiration
- **Files**: `sms_service.py`
- **Configuration**: Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
- **Database**: Creates `sms_verifications` table for code management

## Configuration Guide
Detailed setup instructions available in `INTEGRATION_GUIDE.md`
Example environment variables in `.env.example`