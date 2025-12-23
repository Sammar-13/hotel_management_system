# Hotel Room Booking System – Hotel Miramar SG

This is a comprehensive, production-ready Python Django web application designed for a university final year project. It implements a modern, interactive, and well-structured hotel room booking system with distinct user roles, advanced room management, and a robust booking workflow.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Superuser Credentials](#superuser-credentials)
- [Media & Static Files](#media--static-files)
- [Running the Application](#running-the-application)
- [UI/UX & Design Notes](#uiux--design-notes)

## Features

### User Roles
-   **Guest User**: View home page, hotel information, read-only room listings, nearby tourist places, hotel location (Google Maps embed), Contact Us (send inquiry).
-   **Registered User**: User Registration, Login/Logout, Forgot Password (not implemented in detail in this initial version, but Django's auth system provides the foundation), Profile Update. After login, users can search rooms, view room details, book rooms (date-based), view booked rooms, cancel bookings, and leave feedback.
-   **Admin**: Secure login, Add/Update/Delete Rooms, Upload room images, Approve/Disapprove bookings, Manage registered users, Manage feedback, Manage homepage slider images, View booking reports (basic view), Update admin profile, Logout.

### Core Functionality
-   **Room Module**: Beautiful room cards displaying image, name, price, facilities (icons), availability, "View Details" and "Book Now" buttons. Detailed room page with image gallery (carousel), full description, amenities icons, booking form.
-   **Booking System**: Date-based room availability, booking creation, and cancellation. Admin approval workflow for bookings.
-   **Feedback System**: Registered users can leave feedback on their bookings.
-   **Contact Us**: Guests and registered users can send inquiries.
-   **Homepage Slider**: Dynamic, image-based slider for promotions or featured content.
-   **Search & Filters**: Basic search and filtering options for rooms (by type, price, amenities).

## Tech Stack

-   **Backend**: Python Django (latest stable)
-   **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
-   **Database**: SQLite (default Django)
-   **Authentication**: Django Auth System (customized `User` model)
-   **Media Handling**: Django Media Files
-   **Admin Panel**: Django Admin (customized)

## Project Structure

```
hotel-miramar-sg/
├── hotel_miramar_sg/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hotel/                            # Core hotel app (home, about, contact, feedback)
│   ├── migrations/
│   ├── static/
│   ├── templates/hotel/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
├── users/                            # User management app (auth, profiles)
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── createsuperuser_if_not_exists.py
│   ├── templates/users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── rooms/                            # Room management app
│   ├── migrations/
│   ├── templates/rooms/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── booking/                          # Booking management app
│   ├── migrations/
│   ├── templates/booking/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/                        # Base templates
│   └── base.html
├── static/                           # Project-wide static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── default_hero.jpg
│       ├── default_room.jpg
│       ├── default_room_detail.jpg
│       └── default_profile.png
├── media/                            # User-uploaded media files
│   ├── profile_images/
│   ├── rooms/
│   │   └── gallery/
│   └── slider/
├── manage.py                         # Django's command-line utility
└── README.md
```

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

1.  **Clone the Repository (if applicable):**
    ```bash
    # If using Git
    git clone <repository_url>
    cd hotel-miramar-sg
    ```

2.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    Install Django and other necessary packages.
    ```bash
    pip install Django
    # Add any other packages here, e.g., pip install Pillow (for image handling)
    ```
    *Note: Pillow is recommended for image handling with Django's ImageField.*

5.  **Database Migrations:**
    Apply the initial database migrations to create the necessary tables.
    ```bash
    python manage.py makemigrations users rooms booking hotel
    python manage.py migrate
    ```

6.  **Create Superuser (Automated):**
    A custom management command is provided to automatically create the superuser.
    ```bash
    python manage.py createsuperuser_if_not_exists
    ```

## Superuser Credentials

The automated superuser creation uses the following credentials:

-   **Username**: `sammar`
-   **Email**: `sammarabbas9939@gmail.com`
-   **Password**: `9604959939`

You can use these to log into the Django admin panel (`/admin/`).

## Media & Static Files

-   **Placeholder Images**: The `media/` and `static/images/` directories contain placeholder images. For a production-ready setup, these should be replaced with actual high-quality, AI-generated hotel and room images.
    -   `media/rooms/`: Main images for room listings.
    -   `media/rooms/gallery/`: Additional images for room detail galleries.
    -   `media/slider/`: Images for the homepage carousel.
    -   `media/profile_images/`: User profile pictures.
    -   `static/images/`: Default images (e.g., `default_hero.jpg`, `default_room.jpg`, `default_profile.png`).
-   **Static Files Collection**: For deployment, you will need to collect static files:
    ```bash
    python manage.py collectstatic
    ```

## Running the Application

To run the development server:

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/`.

## UI/UX & Design Notes

-   **Responsiveness**: The frontend is built with Bootstrap 5, ensuring full responsiveness across mobile, tablet, and desktop devices.
-   **Modern Design**: Features a clean layout, attractive color palette, and professional typography.
-   **Interactivity**: Includes smooth animations, hover effects, and interactive elements.
-   **Icons**: Utilizes Bootstrap Icons for amenities and other UI elements.
-   **Image Generation**: All images are intended to be AI-generated and dynamically linked within the templates, creating a realistic and professional hotel website appearance. Replace the placeholder images in the `media/` and `static/images/` directories with your generated content for the best visual experience.
