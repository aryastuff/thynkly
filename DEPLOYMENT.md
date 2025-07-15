# Thynkly Deployment Guide

This guide will help you deploy Thynkly to various platforms including GitHub, Render, Heroku, and Railway.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database (for production)
- Git for version control

## Local Development Setup

1. **Extract the project files** to your desired directory
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies** (copy requirements_manual.txt to requirements.txt first):
   ```bash
   cp requirements_manual.txt requirements.txt
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add:
   ```
   SESSION_SECRET=your-very-secure-secret-key-here
   DATABASE_URL=sqlite:///thynkly.db
   ```
5. **Run the application**:
   ```bash
   python main.py
   ```

## GitHub Upload

1. **Initialize Git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Thynkly innovator matching platform"
   ```

2. **Create a new repository on GitHub** and push:
   ```bash
   git remote add origin https://github.com/yourusername/thynkly.git
   git branch -M main
   git push -u origin main
   ```

**Important Note for GitHub Pages**: This Flask application cannot run directly on GitHub Pages as it requires a server. GitHub Pages only serves static HTML/CSS/JS files. The repository includes a static landing page in the `docs/` folder that explains the deployment options. To actually run the application, deploy to Render, Heroku, Railway, or similar platforms.

## Render Deployment

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Configure build settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT main:app`
4. **Add environment variables**:
   - `SESSION_SECRET`: Generate a secure random string
   - `DATABASE_URL`: Use Render's PostgreSQL add-on
5. **Deploy** and test your application

## Heroku Deployment

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```
2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```
3. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set SESSION_SECRET=your-secure-secret-key
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```

## Railway Deployment

1. **Install Railway CLI** and login:
   ```bash
   npm install -g @railway/cli
   railway login
   ```
2. **Initialize project**:
   ```bash
   railway init
   ```
3. **Add PostgreSQL**:
   ```bash
   railway add postgresql
   ```
4. **Set environment variables**:
   ```bash
   railway variables set SESSION_SECRET=your-secure-secret-key
   ```
5. **Deploy**:
   ```bash
   railway up
   ```

## Environment Variables

### Required Variables

- `SESSION_SECRET`: A secure random string for session management
- `DATABASE_URL`: PostgreSQL connection string (automatically set by cloud providers)

### Optional Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `False` for production

## Database Setup

The application will automatically create database tables on first run. For production:

1. **PostgreSQL is recommended** over SQLite
2. **Database migrations** are handled automatically by SQLAlchemy
3. **Connection pooling** is configured for production use

## Troubleshooting

### Common Issues

1. **SocketIO Connection Issues**:
   - Ensure you're using `eventlet` worker class with Gunicorn
   - Check that WebSocket support is enabled on your platform

2. **Database Connection Issues**:
   - Verify your `DATABASE_URL` is correctly set
   - Ensure PostgreSQL addon is properly configured

3. **Static Files Not Loading**:
   - Check that static files are included in your deployment
   - Verify file paths are correct

### Production Checklist

- [ ] `SESSION_SECRET` is set to a secure random value
- [ ] `DATABASE_URL` points to PostgreSQL database
- [ ] `FLASK_ENV` is set to `production`
- [ ] `FLASK_DEBUG` is set to `False`
- [ ] Dependencies are installed from `requirements.txt`
- [ ] Database tables are created automatically
- [ ] WebSocket support is enabled for real-time features

## File Structure for Upload

Make sure your project contains these files:

```
thynkly/
├── app.py
├── main.py
├── wsgi.py
├── models.py
├── routes.py
├── compatibility.py
├── requirements.txt (copy from requirements_manual.txt)
├── Procfile
├── runtime.txt
├── render.yaml
├── app.json
├── .env.example
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── static/
│   ├── css/style.css
│   └── js/
│       ├── main.js
│       └── socket.js
└── templates/
    ├── base.html
    ├── signin.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    ├── notifications.html
    └── chat.html
```

## Support

If you encounter issues during deployment, check:

1. Application logs on your hosting platform
2. Database connection status
3. Environment variables are correctly set
4. All dependencies are installed

For additional support, refer to the platform-specific documentation or create an issue in the repository.