# Thynkly - Innovator Matching Platform

Thynkly is a Flask-based web application that connects innovators based on their fields of work, keywords, and interests. The platform features user authentication, compatibility scoring, collaboration requests, and real-time messaging capabilities.

## Features

- **User Authentication**: Secure registration and login system
- **Smart Matching**: AI-based compatibility scoring algorithm
- **Collaboration Requests**: Send and manage collaboration requests
- **Real-time Chat**: Live messaging between approved collaborators
- **Field-based Matching**: Connect with people in specific fields:
  - Entrepreneurship
  - Computer Science
  - Fintech
  - Healthtech
  - Design
  - Aerospace
  - Others
- **Keyword Search**: Find innovators based on specific keywords and interests
- **Responsive Design**: Modern UI with Bootstrap 5 and custom styling

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: PostgreSQL (production) / SQLite (development)
- **Real-time**: Socket.IO for live chat and notifications
- **Deployment**: Gunicorn WSGI server

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL (for production)

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd thynkly
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python main.py
   ```

### Production Deployment

#### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn --bind 0.0.0.0:$PORT main:app`
5. Add environment variables:
   - `SESSION_SECRET`: A secure random string
   - `DATABASE_URL`: Your PostgreSQL connection string

#### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Set the start command: `gunicorn --bind 0.0.0.0:$PORT main:app`
3. Add environment variables as needed

#### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn main:app
   ```
2. Push to Heroku and configure environment variables

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Session secret key for Flask
SESSION_SECRET=your-secure-secret-key-here

# Database configuration
DATABASE_URL=postgresql://username:password@localhost/thynkly

# For development (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

## Project Structure

```
thynkly/
├── app.py              # Flask application factory
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Route handlers
├── compatibility.py    # Compatibility scoring algorithm
├── static/             # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       └── socket.js
├── templates/          # HTML templates
│   ├── base.html
│   ├── signin.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── notifications.html
│   └── chat.html
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## API Documentation

### Authentication Endpoints

- `POST /signin` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Main Application Endpoints

- `GET /` - Redirect to dashboard or signin
- `GET /dashboard` - Main dashboard with innovator listings
- `GET /profile` - User profile page
- `POST /profile/edit` - Update user profile
- `GET /notifications` - View collaboration requests
- `POST /request_collaboration` - Send collaboration request
- `POST /respond_request` - Approve/decline collaboration request
- `GET /chat` - Real-time chat interface

### Socket.IO Events

- `join` - Join a chat room
- `leave` - Leave a chat room
- `send_message` - Send a message
- `receive_message` - Receive a message

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `full_name`
- `field_of_work`
- `keywords`
- `interests`
- `bio`
- `created_at`

### Collaboration Requests Table
- `id` (Primary Key)
- `requester_id` (Foreign Key)
- `recipient_id` (Foreign Key)
- `message`
- `status` (pending/approved/declined)
- `created_at`
- `updated_at`

### Messages Table
- `id` (Primary Key)
- `sender_id` (Foreign Key)
- `recipient_id` (Foreign Key)
- `content`
- `timestamp`
- `is_read`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please contact the development team or create an issue in the repository.