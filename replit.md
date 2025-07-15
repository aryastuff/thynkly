# Thynkly - Replit Configuration

## Overview

Thynkly is a Flask-based web application that connects innovators based on their fields of work, keywords, and interests. The application features user authentication, compatibility scoring, collaboration requests, and real-time messaging capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite for development (configurable via DATABASE_URL environment variable)
- **Authentication**: Flask-Login for session management
- **Real-time Communication**: Flask-SocketIO for WebSocket support
- **Password Security**: Werkzeug for password hashing

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **UI Framework**: Bootstrap 5 for responsive design
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript with Socket.IO client for real-time features

### Database Schema
- **Users**: Stores user profiles including bio, field of work, keywords, and interests
- **CollaborationRequest**: Manages collaboration requests between users (pending/approved/declined)
- **Message**: Handles chat messages between approved collaborators
- **Project**: Stores user projects with support for Replit and Google Drive integration

## Key Components

### User Management
- Registration and authentication system
- Profile management with editable preferences
- Password hashing and secure session management

### Compatibility System
- Algorithm that calculates compatibility scores based on:
  - Field of work similarity (30% weight)
  - Keyword overlap (40% weight)
  - Interest overlap (30% weight)
- Search functionality to filter compatible users

### Collaboration Workflow
- Users can send collaboration requests to other users
- Recipients can approve or decline requests
- Only approved collaborators can access messaging features

### Real-time Messaging
- Socket.IO integration for live chat
- Message persistence in database
- Real-time notifications for collaboration requests

### Project Management
- Users can upload projects from Replit or Google Drive
- Project cards display with thumbnails, descriptions, and tags
- Projects are visible on user detail pages
- Support for project URLs, descriptions, and categorization

### UI/UX Features
- Responsive design with Bootstrap 5
- Contrast-based text coloring (dark backgrounds use white text, light backgrounds use dark text)
- Modern gradient backgrounds and card-based layouts
- Auto-dismissing alerts and form validation
- Clickable dashboard tiles for detailed user views
- Interactive project cards with hover effects and external links

## Data Flow

1. **User Registration**: New users create accounts with profile information
2. **Compatibility Calculation**: System calculates compatibility scores between users
3. **Discovery**: Users browse compatible matches on dashboard
4. **Detailed View**: Users can click on dashboard tiles to view detailed profiles and projects
5. **Project Management**: Users can add, view, and manage their projects in the profile section
6. **Collaboration Request**: Users send requests to potential collaborators
7. **Approval Process**: Recipients approve/decline requests via notifications page
8. **Messaging**: Approved collaborators can chat in real-time

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: User session management
- Flask-SocketIO: WebSocket support
- Werkzeug: Password hashing and WSGI utilities

### Frontend Libraries
- Bootstrap 5: UI framework (CDN)
- Font Awesome: Icons (CDN)
- Socket.IO Client: Real-time communication

### Database
- SQLite: Default development database
- Configurable for production databases via DATABASE_URL environment variable

## Deployment Strategy

### Development Setup
- Uses SQLite database for easy local development
- Debug mode enabled in main.py
- Session secret configurable via SESSION_SECRET environment variable

### Production Considerations
- Database URL configurable via environment variables
- ProxyFix middleware for reverse proxy deployments
- Connection pooling with pool_recycle and pool_pre_ping options
- CORS enabled for Socket.IO connections

### File Structure
- `app.py`: Application factory and configuration
- `models.py`: Database models
- `routes.py`: HTTP route handlers
- `compatibility.py`: Compatibility scoring algorithm
- `templates/`: HTML templates
- `static/`: CSS and JavaScript assets
- `main.py`: Application entry point

The application is designed to be easily deployable on platforms like Replit, Render, or similar hosting services with minimal configuration changes.