​# OnlineShop Project

This is an online shopping platform built using Django and Django REST Framework (DRF). It allows customers to browse products, add them to their cart, and complete purchases. Vendors can manage their products and view orders, while admins have a dashboard for managing users, products, and the overall platform.

## Project Overview

The **OnlineShop** platform is designed for both customers and vendors, allowing users to register, browse products, add items to their shopping cart, and make purchases. Vendors can manage their products and monitor orders via a vendor dashboard. Administrators can manage users, products, and vendors from a central dashboard.

## Features

- Customer registration and login
- Vendor management for product listings
- Shopping cart functionality
- Order management for vendors
- Admin dashboard for managing the platform
- Product search and filtering
- API endpoints using Django Rest Framework (DRF)

## Project Structure
onlineshop/
│
├── src/                           # Main project directory
│   ├── cart/                      # Shopping cart app
│   │   ├── migrations/            # Database migrations for cart app
│   │   ├── models.py              # Cart-related models
│   │   ├── views.py               # Views for cart functionality
│   │   ├── urls.py                # URLs for cart app
│   │
│   ├── customers/                 # Customer-related app
│   │   ├── migrations/            # Database migrations for customers app
│   │   ├── models.py              # Customer-related models (profile, orders, etc.)
│   │   ├── views.py               # Views for customer management
│   │   ├── urls.py                # URLs for customers app
│   │
│   ├── dashboard/                 # Admin and vendor dashboard app
│   │   ├── migrations/            # Database migrations for dashboard app
│   │   ├── models.py              # Dashboard-related models
│   │   ├── views.py               # Views for managing platform (admin, vendor)
│   │   ├── urls.py                # URLs for dashboard app
│   │
│   ├── website/                   # Public-facing website app
│   │   ├── migrations/            # Database migrations for website app
│   │   ├── models.py              # Models for product listings, categories
│   │   ├── views.py               # Views for browsing products
│   │   ├── urls.py                # URLs for website app
│   │
│   ├── vendors/                   # Vendor-specific app
│   │   ├── migrations/            # Database migrations for vendors app
│   │   ├── models.py              # Models for vendor-related data
│   │   ├── views.py               # Views for vendors managing products
│   │   ├── urls.py                # URLs for vendors app
│   │
│   ├── accounts/                  # User authentication and account management
│   │   ├── migrations/            # Database migrations for accounts app
│   │   ├── models.py              # Models for user profiles, authentication
│   │   ├── views.py               # Views for login, registration, etc.
│   │   ├── urls.py                # URLs for accounts app
│   │
│   ├── manage.py                  # Django management script
│   ├── settings.py                # Global settings for the project
│   └── tests/                     # Tests directory
│       ├── cart/                  # Tests for cart app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for cart models
│       ├── customers/             # Tests for customers app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for customer models
│       ├── dashboard/             # Tests for dashboard app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for dashboard models
│       ├── website/               # Tests for website app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for website models
│       ├── vendors/               # Tests for vendors app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for vendor models
│       │   └── test_views.py      # Unit tests for vendor views
│       ├── accounts/              # Tests for accounts app
│       │   ├── __init__.py        # Initialization for tests module
│       │   ├── test_models.py     # Unit tests for accounts models
│       │   └── test_views.py      # Unit tests for accounts views
├── .env                           # Environment variables (for local development)
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation


