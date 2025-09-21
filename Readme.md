# Django Trading School

Welcome to Django Trading School – an innovative platform for learning about trading and financial markets.

**Important Notice:**

1. This repository contains an early version of the Django Trading School project. It may not represent the latest features and improvements.

2. The project uses SQLite3 as the default database for development purposes. In a production environment, consider using a more robust database like PostgreSQL or MySQL for better performance and scalability.

## Getting Started


## Key Features

### User Management and Permissions

- **User Roles:** The project implements a comprehensive user role system with four levels of permissions: Superuser, Staff, Has_Right_Sign, Blocked, and Basic_User. Each role has distinct access and privileges tailored to their needs.

### Advanced Admin Panel with Jazzmin

- **Admin Enhancements:** The project utilizes the Jazzmin package to enhance the default Django admin panel. Jazzmin offers a modern and customizable interface for efficient administration of your application.

### Membership Plans and Course Access

- **Membership Plans:** Every user profile is associated with a membership plan, which determines their access to specific courses. This granular approach ensures that users only see courses relevant to their plan.

### Intelligent Scheduler for User Management

- **Auto-Blocking:** A scheduler is implemented to automatically block users who remain inactive for three consecutive months. This ensures the community remains engaged and active.

### Interactive Rating System

- **Lecture and Course Ratings:** Users can provide ratings and reviews for both individual lectures and entire courses. This interactive rating system helps users make informed decisions about which content to engage with.

### Ranking System and User Activation

- **User Activation:** A ranking system encourages user engagement by rewarding active participation. Users can climb the ranks based on their contributions and interactions on the platform.

## Getting Started

Follow these steps to set up the Django Trading School project locally and start exploring its features.

1. Clone the repository: `git clone https://github.com/EngAhmedElBayoumi/Django-trading-school.git`

2. Install dependencies: `pip install -r requirements.txt`

3. Configure your database settings in `settings.py`.

4. Apply database migrations: `python manage.py migrate`

5. Run the development server: `python manage.py runserver`

6. Access the admin panel at `http://127.0.0.1:8000/admin/` and use your superuser credentials to log in.

## Contribution and Feedback

We welcome contributions and feedback from the community. If you have suggestions, bug reports, or feature requests, please open an issue on our GitHub repository.


Thank you for considering Django Trading School for your trading and financial markets education. We look forward to your involvement and success on our platform!


