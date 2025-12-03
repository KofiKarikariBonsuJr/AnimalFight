# 🚀 Project 14 - Production Deployment Guide

This guide walks you through deploying your FastAPI Calculator application to a production server with full security, automatic HTTPS, and CI/CD automation.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Part 1: Local Setup](#part-1-local-setup)
3. [Part 2: Docker Hub Configuration](#part-2-docker-hub-configuration)
4. [Part 3: GitHub Actions CI/CD](#part-3-github-actions-cicd)
5. [Part 4: Server Setup](#part-4-server-setup)
6. [Part 5: Security Hardening](#part-5-security-hardening)
7. [Part 6: Application Deployment](#part-6-application-deployment)
8. [Part 7: Domain & HTTPS](#part-7-domain--https)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

1. **GitHub Account** - For code repository and CI/CD
2. **Docker Hub Account** - For container image storage
3. **Digital Ocean Account** - For server hosting ($7/month or $200 credit with [GitHub Student Developer Pack](https://education.github.com/pack))
4. **Domain Name** - Free .me domain with GitHub Student Pack or purchase ($10-20/year)

### Local Requirements

- Git installed
- Docker Desktop installed (for testing)
- SSH client (built into Windows 10+, macOS, Linux)
- Text editor (VS Code recommended)

---

## Part 1: Local Setup

### Step 1.1: Clone and Test Locally

```bash
# Navigate to your project directory
cd c:\Users\zouba\project14\project14

# Test the application locally
docker-compose up --build

# Open browser to http://localhost:8000
# Test registration, login, and calculations
# Press Ctrl+C to stop when done
```

### Step 1.2: Verify Git Repository

```bash
# Check Git status
git status

# Check remote repository
git remote -v

# Should show: origin  https://github.com/Zoubaiir/project14.git
```

---

## Part 2: Docker Hub Configuration

### Step 2.1: Create Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com/)
2. Click "Sign Up"
3. Create account with username (remember this - you'll need it)
4. Verify your email

### Step 2.2: Create Access Token

1. Log into Docker Hub
2. Click your username → Account Settings
3. Navigate to Security → New Access Token
4. Name: `GitHub Actions CI/CD`
5. Permissions: `Read, Write, Delete`
6. Copy the token (you won't see it again!)

---

## Part 3: GitHub Actions CI/CD

### Step 3.1: Add GitHub Secrets

1. Go to your GitHub repository: `https://github.com/Zoubaiir/project14`
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add two secrets:

   **Secret 1:**
   - Name: `DOCKER_USERNAME`
   - Value: Your Docker Hub username

   **Secret 2:**
   - Name: `DOCKER_PASSWORD`
   - Value: Your Docker Hub access token

### Step 3.2: Test GitHub Actions

```bash
# Commit the new CI/CD workflow
git add .github/workflows/docker-build-deploy.yml
git add .env.example
git add docker-compose.prod.yml
git add Caddyfile
git commit -m "Add CI/CD and production configuration"
git push origin main

# Go to GitHub repository → Actions tab
# Watch the workflow run (tests → build → push to Docker Hub)
```

### Step 3.3: Verify Docker Hub

1. Go to Docker Hub → Repositories
2. You should see `your-username/project14`
3. Verify the `latest` tag exists

---

## Part 4: Server Setup

### Step 4.1: Create Digital Ocean Droplet

1. Log into [Digital Ocean](https://www.digitalocean.com/)
2. Click "Create" → "Droplets"
3. Choose configuration:
   - **Image**: Ubuntu 24.04 (LTS) x64
   - **Plan**: Basic
   - **CPU options**: Regular (Disk type: SSD)
   - **Size**: $7/month (1 GB RAM / 1 CPU / 25 GB SSD / 1000 GB transfer)
   - **Datacenter**: Choose closest to you
   - **Authentication**: SSH Key (recommended) or Password
4. **Hostname**: `project14-prod`
5. Click "Create Droplet"
6. Wait for creation (2-3 minutes)
7. **Copy the server IP address** - You'll need this!

### Step 4.2: Setup SSH Key (If Not Already Done)

**On Windows:**

```powershell
# Open PowerShell
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter for default location
# Press Enter twice for no passphrase (or set one for extra security)

# Display public key
cat ~/.ssh/id_ed25519.pub

# Copy the output
```

**Add to Digital Ocean:**
1. Digital Ocean → Settings → Security → SSH Keys
2. Click "Add SSH Key"
3. Paste your public key
4. Name it (e.g., "My Laptop")

### Step 4.3: First Connection

```bash
# Replace YOUR_SERVER_IP with actual IP
ssh root@YOUR_SERVER_IP

# Type 'yes' to continue connecting
# You should now be logged into your server!
```

---

## Part 5: Security Hardening

**Follow the [mywebclass_hosting guide](https://github.com/kaw393939/mywebclass_hosting) for complete security setup. Here's a summary:**

### Step 5.1: System Updates

```bash
# Update system packages
apt update && apt upgrade -y

# Install essential tools
apt install -y curl wget git ufw fail2ban unattended-upgrades
```

### Step 5.2: Create Non-Root User

```bash
# Create user (replace 'yourname' with your preferred username)
adduser yourname

# Add to sudo group
usermod -aG sudo yourname

# Setup SSH for new user
mkdir -p /home/yourname/.ssh
cp /root/.ssh/authorized_keys /home/yourname/.ssh/
chown -R yourname:yourname /home/yourname/.ssh
chmod 700 /home/yourname/.ssh
chmod 600 /home/yourname/.ssh/authorized_keys
```

### Step 5.3: Configure Firewall (UFW)

```bash
# Allow SSH (IMPORTANT - do this first!)
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 443/udp

# Enable firewall
ufw --force enable

# Check status
ufw status
```

### Step 5.4: Configure Fail2Ban

```bash
# Start and enable Fail2Ban
systemctl start fail2ban
systemctl enable fail2ban

# Check status
fail2ban-client status

# Check SSH jail
fail2ban-client status sshd
```

### Step 5.5: Secure SSH

```bash
# Edit SSH config
nano /etc/ssh/sshd_config

# Change these settings:
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes

# Save and exit (Ctrl+X, Y, Enter)

# Restart SSH
systemctl restart sshd
```

### Step 5.6: Test New User Connection

**Open a NEW terminal (keep the old one open as backup!):**

```bash
# Try connecting with new user
ssh yourname@YOUR_SERVER_IP

# Test sudo access
sudo apt update
```

**If this works, you can close the root session. If not, use the root session to fix it!**

---

## Part 6: Application Deployment

### Step 6.1: Install Docker

```bash
# Log in as your non-root user
ssh yourname@YOUR_SERVER_IP

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group to take effect
exit
ssh yourname@YOUR_SERVER_IP

# Verify Docker installation
docker --version
docker compose version
```

### Step 6.2: Prepare Application Directory

```bash
# Create application directory
mkdir -p ~/project14
cd ~/project14

# Create .env file with production settings
nano .env
```

**Copy and modify the following (REPLACE ALL PLACEHOLDERS!):**

```env
# Docker Hub Configuration
DOCKER_USERNAME=your-dockerhub-username

# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_STRONG_DB_PASSWORD_HERE@db:5432/fastapi_db
TEST_DATABASE_URL=postgresql://postgres:YOUR_STRONG_DB_PASSWORD_HERE@db:5432/fastapi_test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD_HERE
POSTGRES_DB=fastapi_db

# JWT Configuration (Generate these: openssl rand -hex 32)
JWT_SECRET_KEY=YOUR_GENERATED_SECRET_KEY_HERE_MIN_32_CHARS
JWT_REFRESH_SECRET_KEY=YOUR_GENERATED_REFRESH_SECRET_KEY_HERE_MIN_32_CHARS
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Hashing
BCRYPT_ROUNDS=12

# Python Configuration
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# Domain Configuration
DOMAIN=your-actual-domain.com
EMAIL=your-email@example.com

# PgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin@your-domain.com
PGADMIN_DEFAULT_PASSWORD=YOUR_STRONG_ADMIN_PASSWORD_HERE
```

**Save and exit (Ctrl+X, Y, Enter)**

### Step 6.3: Generate Secure Secrets

```bash
# Generate JWT secrets
openssl rand -hex 32  # Use this for JWT_SECRET_KEY
openssl rand -hex 32  # Use this for JWT_REFRESH_SECRET_KEY

# Update your .env file with these values
nano .env
```

### Step 6.4: Download Configuration Files

```bash
# Download docker-compose file
curl -o docker-compose.yml https://raw.githubusercontent.com/Zoubaiir/project14/main/docker-compose.prod.yml

# Download Caddyfile
curl -o Caddyfile https://raw.githubusercontent.com/Zoubaiir/project14/main/Caddyfile
```

### Step 6.5: Start the Application

```bash
# Pull the latest image
docker compose pull

# Start services
docker compose up -d

# Check status
docker compose ps

# Check logs
docker compose logs -f web
# Press Ctrl+C to exit logs
```

### Step 6.6: Verify Application

```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

---

## Part 7: Domain & HTTPS

### Step 7.1: Configure Domain DNS

1. Log into your domain registrar (Namecheap, GitHub Student Pack, etc.)
2. Go to DNS settings for your domain
3. Add/Update these records:

   **A Record:**
   - Host: `@`
   - Value: `YOUR_SERVER_IP`
   - TTL: Automatic or 300

   **A Record (for www):**
   - Host: `www`
   - Value: `YOUR_SERVER_IP`
   - TTL: Automatic or 300

4. Save changes (DNS propagation takes 5-60 minutes)

### Step 7.2: Verify DNS Propagation

```bash
# Check from your local machine
nslookup your-domain.com

# Should show your server IP
```

### Step 7.3: Update Server Configuration

```bash
# On your server
cd ~/project14

# Update .env with your actual domain
nano .env

# Change:
# DOMAIN=your-actual-domain.com
# EMAIL=your-email@example.com

# Restart services
docker compose down
docker compose up -d

# Watch Caddy get the certificate
docker compose logs -f caddy
```

### Step 7.4: Test HTTPS

1. Open browser to `https://your-domain.com`
2. Should see your application with valid HTTPS!
3. Check certificate (click padlock icon)

---

## 🎉 Deployment Complete!

Your application is now:
- ✅ Running in production
- ✅ Protected with automatic HTTPS
- ✅ Secured with firewall and Fail2Ban
- ✅ Automatically updating via Watchtower
- ✅ Building and deploying via GitHub Actions

---

## Automatic Updates

Watchtower checks Docker Hub every 5 minutes for new images:

```bash
# Make code changes locally
git add .
git commit -m "Update feature"
git push origin main

# GitHub Actions builds and pushes to Docker Hub
# Watchtower detects new image (within 5 minutes)
# Application automatically updates!

# Watch the update happen
docker compose logs -f watchtower
```

---

## Useful Commands

### Application Management

```bash
# View logs
docker compose logs -f web

# Restart application
docker compose restart web

# Stop all services
docker compose down

# Start all services
docker compose up -d

# Update to latest image manually
docker compose pull
docker compose up -d
```

### Database Management

```bash
# Access database
docker compose exec db psql -U postgres -d fastapi_db

# Backup database
docker compose exec db pg_dump -U postgres fastapi_db > backup.sql

# Restore database
docker compose exec -T db psql -U postgres fastapi_db < backup.sql
```

### System Maintenance

```bash
# Check disk space
df -h

# Clean up old Docker images
docker system prune -a

# View resource usage
docker stats

# Check UFW status
sudo ufw status

# Check Fail2Ban status
sudo fail2ban-client status
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
docker compose logs web

# Check if database is ready
docker compose logs db

# Verify environment variables
cat .env

# Restart services
docker compose down
docker compose up -d
```

### HTTPS Not Working

```bash
# Check Caddy logs
docker compose logs caddy

# Verify DNS is pointing to your server
nslookup your-domain.com

# Ensure ports are open
sudo ufw status

# Check if Caddy can reach the web service
docker compose exec caddy wget -O- http://web:8000/health
```

### Watchtower Not Updating

```bash
# Check Watchtower logs
docker compose logs watchtower

# Manually trigger update
docker compose pull
docker compose up -d
```

### Can't SSH Into Server

```bash
# Check if SSH is allowed in firewall
sudo ufw status

# Check SSH service status
sudo systemctl status sshd

# Check Fail2Ban (you might be banned!)
sudo fail2ban-client status sshd
sudo fail2ban-client unban YOUR_IP
```

### Database Connection Issues

```bash
# Check if database is running
docker compose ps db

# Check database logs
docker compose logs db

# Verify connection string in .env
cat .env | grep DATABASE_URL

# Test database connection
docker compose exec db psql -U postgres -d fastapi_db -c "SELECT version();"
```

---

## Security Best Practices

1. **Regularly update your server:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Monitor failed login attempts:**
   ```bash
   sudo fail2ban-client status sshd
   ```

3. **Check Docker security updates:**
   ```bash
   docker compose pull
   docker compose up -d
   ```

4. **Backup your database regularly:**
   ```bash
   # Create backup script
   mkdir -p ~/backups
   nano ~/backup.sh
   ```

   **backup.sh:**
   ```bash
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   docker compose -f ~/project14/docker-compose.yml exec -T db pg_dump -U postgres fastapi_db > ~/backups/backup_$DATE.sql
   find ~/backups -name "backup_*.sql" -mtime +7 -delete
   ```

   ```bash
   chmod +x ~/backup.sh
   
   # Add to crontab (daily at 2 AM)
   crontab -e
   # Add: 0 2 * * * /home/yourname/backup.sh
   ```

5. **Change default passwords** in `.env`

6. **Review logs regularly:**
   ```bash
   docker compose logs --tail=100 web
   ```

---

## Additional Resources

- **Course Material**: [MyWebClass Hosting Guide](https://github.com/kaw393939/mywebclass_hosting)
- **Digital Ocean Docs**: [digitalocean.com/docs](https://docs.digitalocean.com/)
- **Docker Docs**: [docs.docker.com](https://docs.docker.com/)
- **Caddy Docs**: [caddyserver.com/docs](https://caddyserver.com/docs/)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the [mywebclass_hosting documentation](https://github.com/kaw393939/mywebclass_hosting)
3. Check Docker and application logs
4. Verify all configuration files
5. Ensure all environment variables are set correctly

---

## License

This project is for educational purposes as part of the MyWebClass course.

---

**Last Updated**: December 2025
**Version**: 1.0.0
