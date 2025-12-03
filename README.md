# 🚀 Project 14 - FastAPI Calculator with Production Deployment

A fully functional FastAPI web application with user authentication, calculator functionality, and complete production deployment setup using Docker, CI/CD, and automatic HTTPS.

## 📚 Documentation

- **[🚀 Quick Start Guide](./QUICKSTART.md)** - Get started in 10 minutes
- **[📖 Full Deployment Guide](./DEPLOYMENT.md)** - Complete production deployment
- **[🛡️ Server Setup Guide](./SERVER_SETUP.md)** - Detailed server security setup
- **[📦 Project Setup](./docs/00-course-overview.md)** - Development documentation

## ✨ Features

- 🔐 **User Authentication** - JWT-based secure authentication
- 🧮 **Calculator Operations** - Create, read, update, delete calculations
- 🗄️ **PostgreSQL Database** - Robust data persistence
- 🐳 **Docker Ready** - Containerized application
- 🔄 **CI/CD Pipeline** - Automated testing and deployment
- 🔒 **Automatic HTTPS** - Caddy reverse proxy with Let's Encrypt
- 📊 **Database Admin** - PgAdmin interface included
- 🔄 **Auto Updates** - Watchtower for automatic deployments

## 🎯 What You'll Learn

This project demonstrates professional-level skills in:

- ✅ **Full-Stack Development** - Python FastAPI backend with HTML/CSS/JS frontend
- ✅ **DevOps & CI/CD** - GitHub Actions, Docker, automated deployments
- ✅ **Security** - SSH hardening, firewall, Fail2Ban, HTTPS
- ✅ **Cloud Deployment** - Digital Ocean VPS setup and management
- ✅ **Infrastructure as Code** - Docker Compose, Caddy configuration
- ✅ **Database Management** - PostgreSQL, migrations, backups
- ✅ **System Administration** - Linux server, monitoring, maintenance

**Perfect for résumés and technical interviews!**

## 🚦 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Zoubaiir/project14.git
cd project14

# Start with Docker Compose
docker-compose up --build

# Access the application
# Web: http://localhost:8000
# PgAdmin: http://localhost:5050
```

### Production Deployment

See the [Quick Start Guide](./QUICKSTART.md) for a condensed version, or follow the [Complete Deployment Guide](./DEPLOYMENT.md) for detailed instructions.

**Summary:**
1. Create Docker Hub account and GitHub secrets
2. Push code to GitHub (auto-builds and tests)
3. Set up secure Ubuntu server on Digital Ocean
4. Deploy application with one command
5. Configure domain for automatic HTTPS
6. Enjoy automatic updates on every git push!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │  Caddy (443)  │  Automatic HTTPS
            │  Reverse      │  SSL/TLS
            │  Proxy        │  Load Balancer
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │   FastAPI     │  Application Logic
            │   Web App     │  JWT Auth
            │   (8000)      │  REST API
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  PostgreSQL   │  Data Persistence
            │  Database     │  User Management
            │   (5432)      │  Calculations
            └───────────────┘

        ┌─────────────────┐
        │   Watchtower    │  Auto-Update
        │                 │  Container Monitor
        └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL 17** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **JWT** - Secure authentication
- **Bcrypt** - Password hashing

### Frontend
- **HTML/CSS** - Responsive design
- **JavaScript** - Interactive UI
- **Bootstrap** - UI components

### DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Caddy** - Reverse proxy & automatic HTTPS
- **Watchtower** - Automatic container updates

### Infrastructure
- **Ubuntu 24.04 LTS** - Server OS
- **UFW** - Firewall
- **Fail2Ban** - Intrusion prevention
- **Digital Ocean** - Cloud hosting

## 📂 Project Structure

```
project14/
├── app/
│   ├── auth/              # Authentication logic
│   ├── core/              # Configuration
│   ├── models/            # Database models
│   ├── operations/        # Business logic
│   ├── schemas/           # Pydantic schemas
│   ├── database.py        # Database connection
│   └── main.py            # FastAPI application
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── static/                # CSS, JavaScript
├── templates/             # HTML templates
├── docs/                  # Development documentation
├── .github/workflows/     # CI/CD pipelines
├── Dockerfile             # Container definition
├── docker-compose.yml     # Local development
├── docker-compose.prod.yml # Production deployment
├── Caddyfile              # Reverse proxy config
├── requirements.txt       # Python dependencies
├── DEPLOYMENT.md          # Deployment guide
├── SERVER_SETUP.md        # Server setup guide
└── QUICKSTART.md          # Quick start guide
```

## 🔄 CI/CD Pipeline

Every push to `main` triggers:

1. **Testing**
   - Automated pytest suite
   - Code coverage analysis
   - Integration tests with PostgreSQL

2. **Building**
   - Docker image creation
   - Multi-stage optimization
   - Security scanning

3. **Deployment**
   - Push to Docker Hub
   - Tagged with commit SHA
   - Watchtower auto-deploys to server

**Zero downtime deployments!**

## 🔒 Security Features

- ✅ **SSH Hardening** - Key-only authentication, no root login
- ✅ **Firewall** - UFW configured for necessary ports only
- ✅ **Intrusion Prevention** - Fail2Ban blocks brute force attacks
- ✅ **HTTPS** - Automatic SSL/TLS certificates
- ✅ **Secrets Management** - Environment variables for sensitive data
- ✅ **Non-Root Containers** - Docker security best practices
- ✅ **Security Headers** - HSTS, CSP, X-Frame-Options
- ✅ **Rate Limiting** - Caddy-based request throttling

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## 📊 Monitoring & Maintenance

### View Logs
```bash
# Application logs
docker compose logs -f web

# Database logs
docker compose logs -f db

# Caddy logs
docker compose logs -f caddy

# Watchtower logs
docker compose logs -f watchtower
```

### Resource Monitoring
```bash
# Container stats
docker stats

# Disk usage
df -h

# Memory usage
free -h
```

### Database Backup
```bash
# Create backup
docker compose exec db pg_dump -U postgres fastapi_db > backup.sql

# Restore backup
docker compose exec -T db psql -U postgres fastapi_db < backup.sql
```

## 🌟 Production URLs

Once deployed:

- **Main Application**: `https://your-domain.com`
- **API Documentation**: `https://your-domain.com/docs`
- **Health Check**: `https://your-domain.com/health`

## 📖 Course Materials

This project includes comprehensive learning materials:

1. [Course Overview](./docs/00-course-overview.md)
2. [Project Setup](./docs/01-project-setup.md)
3. [Database Models](./docs/02-database-models.md)
4. [Schema Validation](./docs/03-schema-validation.md)
5. [Authentication](./docs/04-authentication.md)
6. [API Endpoints](./docs/05-api-endpoints.md)
7. [Frontend Integration](./docs/06-frontend-integration.md)
8. [Testing](./docs/07-testing.md)
9. [Containerization](./docs/08-containerization.md)

## 🆘 Troubleshooting

### Common Issues

**Application won't start:**
```bash
docker compose logs web
docker compose restart web
```

**Database connection errors:**
```bash
docker compose logs db
docker compose restart db
```

**HTTPS not working:**
```bash
# Check DNS
nslookup your-domain.com

# Check Caddy
docker compose logs caddy
```

**Can't SSH to server:**
```bash
# Check firewall
sudo ufw status

# Check Fail2Ban
sudo fail2ban-client status sshd
```

See [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting) for detailed troubleshooting.

## 🤝 Contributing

This is an educational project. Improvements welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is for educational purposes as part of the MyWebClass course.

## 🙏 Acknowledgments

- **Professor Keith Williams** - [MyWebClass Hosting Guide](https://github.com/kaw393939/mywebclass_hosting)
- **FastAPI Documentation** - [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **Docker Documentation** - [docs.docker.com](https://docs.docker.com/)
- **Digital Ocean Tutorials** - [digitalocean.com/community](https://www.digitalocean.com/community)

## 📞 Support

- **Full Documentation**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Quick Help**: See [QUICKSTART.md](./QUICKSTART.md)
- **Server Setup**: See [SERVER_SETUP.md](./SERVER_SETUP.md)
- **Course Guide**: [MyWebClass Hosting](https://github.com/kaw393939/mywebclass_hosting)

---

**Built with ❤️ for learning DevOps and modern web development**

⭐ Star this repository if you find it helpful!

---

## 🎯 Learning Outcomes

By completing this project, you will have:

- ✅ Deployed a production web application
- ✅ Configured automatic HTTPS with Let's Encrypt
- ✅ Set up CI/CD with GitHub Actions
- ✅ Secured a Linux server (SSH, firewall, Fail2Ban)
- ✅ Implemented containerization with Docker
- ✅ Configured reverse proxy and load balancing
- ✅ Set up automatic deployments with Watchtower
- ✅ Managed PostgreSQL databases in production
- ✅ Implemented JWT authentication
- ✅ Written comprehensive tests
- ✅ Documented infrastructure as code

**This demonstrates real-world DevOps skills valued by employers!**
