Absolutely — here's the updated version of the **`README.md`** without LinkedIn content or issue resolution sections:

````markdown
# Django Billing & Subscription Platform 🧾⚙️

A modular, scalable billing and subscription system built using Django and Django REST Framework — ideal for SaaS platforms needing recurring billing, tax handling, Stripe payments, automated invoicing, and PDF generation.

---

## 🚀 Features

- JWT-based authentication system (register, login, profiles)
- Product and tiered pricing management (admin only)
- Tax rate management
- Subscription lifecycle management (start, cancel)
- Stripe payment integration with webhook handling
- Automatic invoice generation with PDF export (WeasyPrint)
- Manual invoice upload and OCR parsing (Amazon Textract)
- Webhook registration + outbound event POSTs
- Background task processing (Celery + Redis)

---

## 🧱 Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Payments**: Stripe API & Webhooks
- **OCR**: AWS Textract
- **PDF Generation**: WeasyPrint
- **Async Tasks**: Celery + Redis
- **Scheduling**: django-celery-beat
- **Database**: PostgreSQL (via Django ORM)

---

## 🏗️ API Architecture by Phase

| Phase | Description                                                                 |
|-------|-----------------------------------------------------------------------------|
| 1     | Project Initialization & App Setup                                          |
| 2     | JWT Auth System + User Profile App                                          |
| 3     | Product & Pricing Tier App (admin-only access)                              |
| 4     | Taxes App — Tax Rates applied at line item level                            |
| 5     | Subscriptions App — Lifecycle and linking with pricing tiers & customers    |
| 6     | Stripe Integration — PaymentIntent, Customer, Webhooks                      |
| 7     | Invoicing App — Invoice creation + WeasyPrint PDF export                    |
| 8     | Manual Invoices App — Upload & parse via Textract                           |
| 9     | Webhooks App — Register endpoints & send system events (invoice/payment)    |
| 10    | Celery Tasks — Email sending, retries, periodic billing                     |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/billing-system.git
cd billing-system
pip install -r requirements.txt
cp .env.example .env  # Fill in Stripe and AWS keys
````

Configure PostgreSQL, Redis, and set your environment variables accordingly.

---

## 🧪 Running Locally

```bash
# Run migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Start Redis and Celery:

```bash
redis-server
celery -A billing_system worker --loglevel=info
celery -A billing_system beat --loglevel=info
```

---

## 🔐 API Authentication

We use JWT for secure access to all endpoints.

* `POST /api/auth/register/`
* `POST /api/auth/login/`
* Add `Authorization: Bearer <your_token>` to all requests.

---

## 🧾 Core API Endpoints (Summary)

### Auth & Profiles

* `POST /api/auth/register/`
* `POST /api/auth/login/`
* `GET /api/profile/`
* `PATCH /api/profile/`

### Products & Pricing Tiers

* `POST /api/products/` *(admin only)*
* `POST /api/pricing-tiers/` *(admin only)*
* `GET /api/products/`
* `GET /api/pricing-tiers/`

### Tax Rates

* `POST /api/tax-rates/` *(admin only)*
* `GET /api/tax-rates/`

### Subscriptions

* `POST /api/subscriptions/`
* `PATCH /api/subscriptions/{id}/cancel/`
* `GET /api/subscriptions/`

### Payments & Stripe Integration

* `POST /api/payments/initiate/`
* `POST /api/payments/webhook/` *(Stripe posts here)*

### Invoicing

* `GET /api/invoices/`
* `GET /api/invoices/{id}/download/`

### Manual Invoices

* `POST /api/manual-invoices/upload/`
* `GET /api/manual-invoices/{id}/`

### Webhook System

* `POST /api/webhooks/register/`
* Internal: POSTs events like invoice.created, subscription.started, payment.success, etc.

---

## 📂 Folder Structure

```
billing_system/
│
├── users/                # JWT Auth and Profile
├── products/             # Product and PricingTier
├── taxes/                # TaxRate model
├── subscriptions/        # Subscription logic
├── payments/             # Stripe integration
├── invoices/             # Invoice + PDF export
├── manualinvoices/       # Textract-powered manual uploads
├── webhooks/             # Webhook registration and events
├── billing_system/       # Root Django config
└── requirements.txt
```

---

## 📌 Environment Variables

Create a `.env` file or use system-level envs:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

---

## 🧠 Future Enhancements

* Docker setup with Nginx, Gunicorn
* Customer billing dashboard
* Admin analytics dashboard (MRR, ARPU, churn)
* PDF watermarking and email templating

---

