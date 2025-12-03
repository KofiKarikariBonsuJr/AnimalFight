# 🛡️ Server Setup & Security Guide

This guide follows the [mywebclass_hosting](https://github.com/kaw393939/mywebclass_hosting) best practices for setting up a secure production server.

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Digital Ocean account (or similar VPS provider)
- [ ] SSH client installed (built into Windows 10+, macOS, Linux)
- [ ] Domain name (optional but recommended)
- [ ] GitHub Student Developer Pack (optional - for $200 credit)

---

## Part 1: Initial Server Setup (15 minutes)

### Step 1.1: Create Digital Ocean Droplet

1. **Log into Digital Ocean**
   - Visit [digitalocean.com](https://www.digitalocean.com/)
   - Click "Create" → "Droplets"

2. **Choose Image**
   - Distribution: **Ubuntu 24.04 (LTS) x64**
   - Why: Latest long-term support, well-documented

3. **Choose Size**
   - Plan: **Basic**
   - CPU Options: **Regular (SSD)**
   - Size: **$7/month**
     - 1 GB RAM
     - 1 vCPU
     - 25 GB SSD
     - 1000 GB Transfer
   - This is sufficient for multiple small apps!

4. **Choose Datacenter**
   - Pick closest to your target users
   - Recommendation: New York 3, San Francisco 3, or London 1

5. **Authentication**
   - **Recommended:** SSH Key
   - **Alternative:** Password (less secure)

6. **Hostname**
   - Example: `project14-prod`

7. **Create Droplet**
   - Wait 2-3 minutes
   - **Copy your server IP address!**

### Step 1.2: Generate SSH Key (If Not Done)

**On Windows (PowerShell):**

```powershell
# Check if SSH key exists
Test-Path ~/.ssh/id_ed25519.pub

# If false, generate new key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter for default location
# Set a passphrase (recommended) or press Enter twice for none

# Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this entire output
```

**On macOS/Linux:**

```bash
# Check if SSH key exists
ls ~/.ssh/id_ed25519.pub

# If not exists, generate
ssh-keygen -t ed25519 -C "your-email@example.com"

# Display public key
cat ~/.ssh/id_ed25519.pub
# Copy this entire output
```

**Add to Digital Ocean:**

1. Go to Digital Ocean → Settings → Security → SSH Keys
2. Click "Add SSH Key"
3. Paste your public key
4. Name it (e.g., "My Laptop - Windows")
5. Save

### Step 1.3: First Connection

```bash
# Connect as root
ssh root@YOUR_SERVER_IP

# Type 'yes' when asked about fingerprint
# You should see: root@project14-prod:~#
```

---

## Part 2: System Updates & Essential Tools (10 minutes)

### Step 2.1: Update System Packages

```bash
# Update package lists
apt update

# Upgrade all packages
apt upgrade -y

# This may take 5-10 minutes
# You might be prompted about kernel upgrades - choose "Keep current version"
```

### Step 2.2: Install Essential Tools

```bash
# Install security and networking tools
apt install -y \
  curl \
  wget \
  git \
  ufw \
  fail2ban \
  unattended-upgrades \
  apt-transport-https \
  ca-certificates \
  gnupg \
  lsb-release

# Verify installations
curl --version
git --version
ufw version
```

### Step 2.3: Configure Automatic Updates

```bash
# Enable automatic security updates
dpkg-reconfigure -plow unattended-upgrades

# Select "Yes" when prompted

# Verify configuration
cat /etc/apt/apt.conf.d/20auto-upgrades
```

---

## Part 3: User Management & Access Control (10 minutes)

### Step 3.1: Create Non-Root User

```bash
# Create new user (replace 'yourname' with your username)
adduser yourname

# Set a STRONG password
# Fill in user information (can press Enter to skip)

# Add user to sudo group
usermod -aG sudo yourname

# Verify user was created
id yourname
```

### Step 3.2: Setup SSH for New User

```bash
# Create .ssh directory for new user
mkdir -p /home/yourname/.ssh

# Copy authorized keys from root
cp /root/.ssh/authorized_keys /home/yourname/.ssh/

# Set correct permissions
chown -R yourname:yourname /home/yourname/.ssh
chmod 700 /home/yourname/.ssh
chmod 600 /home/yourname/.ssh/authorized_keys

# Verify permissions
ls -la /home/yourname/.ssh
```

### Step 3.3: Test New User (IMPORTANT!)

**Open a NEW terminal window (keep root session open as backup!):**

```bash
# Try connecting as new user
ssh yourname@YOUR_SERVER_IP

# You should connect successfully

# Test sudo access
sudo apt update

# Enter your password
# Should complete without errors
```

**If this works, keep both terminals open for now. If not, use root terminal to troubleshoot!**

---

## Part 4: Firewall Configuration (5 minutes)

### Step 4.1: Configure UFW (Uncomplicated Firewall)

**⚠️ CRITICAL: Follow steps exactly to avoid locking yourself out!**

```bash
# In your NEW USER terminal
# Allow SSH FIRST (port 22)
sudo ufw allow 22/tcp

# Allow HTTP (port 80)
sudo ufw allow 80/tcp

# Allow HTTPS (port 443)
sudo ufw allow 443/tcp
sudo ufw allow 443/udp

# Check rules before enabling
sudo ufw show added

# Enable firewall
sudo ufw --force enable

# Check status
sudo ufw status verbose
```

**Expected output:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
443/udp                    ALLOW IN    Anywhere
```

### Step 4.2: Verify Firewall

```bash
# Test that SSH still works (you should already be connected)
# Try in another terminal
ssh yourname@YOUR_SERVER_IP

# Should still connect fine
```

---

## Part 5: SSH Hardening (10 minutes)

### Step 5.1: Configure SSH Security

```bash
# Backup original SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Edit SSH configuration
sudo nano /etc/ssh/sshd_config
```

**Find and modify these lines (remove # if commented):**

```bash
# Disable root login
PermitRootLogin no

# Disable password authentication
PasswordAuthentication no

# Enable public key authentication
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Disable challenge-response authentication
ChallengeResponseAuthentication no

# Limit authentication attempts
MaxAuthTries 3

# Set login grace time
LoginGraceTime 60

# Disable X11 forwarding (if not needed)
X11Forwarding no

# Enable strict mode
StrictModes yes
```

**Save and exit:** Ctrl+X, then Y, then Enter

### Step 5.2: Test SSH Configuration

```bash
# Test configuration for syntax errors
sudo sshd -t

# Should return nothing (no output = success)

# If there are errors, fix them before continuing!
```

### Step 5.3: Restart SSH Service

```bash
# Restart SSH to apply changes
sudo systemctl restart sshd

# Check SSH status
sudo systemctl status sshd

# Should show "active (running)"
```

### Step 5.4: Verify SSH Access

**Keep your current session open! Open a NEW terminal:**

```bash
# Try connecting again as your user
ssh yourname@YOUR_SERVER_IP

# Should work fine

# Try connecting as root (should fail now)
ssh root@YOUR_SERVER_IP
# Should see: "Permission denied"
```

**✅ If user connection works and root is denied, SSH is properly secured!**

---

## Part 6: Fail2Ban Configuration (10 minutes)

### Step 6.1: Install and Configure Fail2Ban

```bash
# Fail2Ban should already be installed, but verify
sudo systemctl status fail2ban

# Create local configuration
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Edit configuration
sudo nano /etc/fail2ban/jail.local
```

**Find [DEFAULT] section and modify:**

```ini
[DEFAULT]
# Ban for 1 hour
bantime = 3600

# Monitor last 10 minutes
findtime = 600

# Ban after 5 failures
maxretry = 5

# Notification email (optional)
destemail = your-email@example.com
sendername = Fail2Ban
```

**Find [sshd] section and ensure it's enabled:**

```ini
[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s
```

**Save and exit:** Ctrl+X, then Y, then Enter

### Step 6.2: Start and Enable Fail2Ban

```bash
# Start Fail2Ban
sudo systemctl start fail2ban

# Enable to start on boot
sudo systemctl enable fail2ban

# Check status
sudo systemctl status fail2ban

# Should show "active (running)"
```

### Step 6.3: Verify Fail2Ban

```bash
# Check Fail2Ban status
sudo fail2ban-client status

# Check SSH jail specifically
sudo fail2ban-client status sshd

# View banned IPs (should be empty initially)
sudo fail2ban-client status sshd | grep "Banned IP"
```

### Step 6.4: Test Fail2Ban (Optional)

**⚠️ Be careful - don't ban yourself!**

```bash
# View SSH authentication log
sudo tail -f /var/log/auth.log

# In another terminal, try to SSH with wrong password 6 times
# You'll get banned after 5 failures

# To unban yourself (if needed)
sudo fail2ban-client set sshd unbanip YOUR_IP_ADDRESS
```

---

## Part 7: Docker Installation (10 minutes)

### Step 7.1: Install Docker

```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index
sudo apt update

# Install Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# This will take 3-5 minutes
```

### Step 7.2: Configure Docker

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group change to take effect
exit

# Log back in
ssh yourname@YOUR_SERVER_IP

# Verify Docker installation
docker --version
docker compose version

# Test Docker
docker run hello-world

# Should download and run successfully
```

### Step 7.3: Configure Docker for Production

```bash
# Create Docker daemon configuration
sudo nano /etc/docker/daemon.json
```

**Add this configuration:**

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false
}
```

**Save and exit, then restart Docker:**

```bash
# Restart Docker
sudo systemctl restart docker

# Verify configuration
docker info | grep -A 5 "Log"
```

---

## Part 8: System Monitoring & Maintenance

### Step 8.1: Install Monitoring Tools

```bash
# Install htop for process monitoring
sudo apt install -y htop

# Install ncdu for disk usage
sudo apt install -y ncdu

# Run htop to see system resources
htop
# Press q to quit
```

### Step 8.2: Check System Resources

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU info
lscpu

# Check running services
systemctl list-units --type=service --state=running
```

### Step 8.3: Set Up Log Rotation

```bash
# Docker logs are already configured for rotation
# Verify Docker log configuration
sudo cat /etc/docker/daemon.json

# Check system log rotation
ls -la /etc/logrotate.d/

# View logrotate configuration for rsyslog
cat /etc/logrotate.d/rsyslog
```

---

## Part 9: Final Security Checks

### Step 9.1: Verify All Services

```bash
# Check SSH
sudo systemctl status sshd

# Check Fail2Ban
sudo systemctl status fail2ban

# Check Docker
sudo systemctl status docker

# Check UFW
sudo ufw status

# All should show "active (running)" or "active"
```

### Step 9.2: Security Audit

```bash
# Check open ports
sudo ss -tulpn

# Should only see ports: 22, 53 (DNS), and Docker ports when running

# Check failed login attempts
sudo grep "Failed password" /var/log/auth.log | tail -20

# Check Fail2Ban bans
sudo fail2ban-client status sshd
```

### Step 9.3: Create Security Checklist

```bash
# Create a security checklist file
cat > ~/security-checklist.md << 'EOF'
# Security Checklist

## Initial Setup
- [x] System packages updated
- [x] Non-root user created
- [x] SSH key authentication configured
- [x] UFW firewall enabled
- [x] Fail2Ban configured
- [x] Docker installed

## SSH Security
- [x] Root login disabled
- [x] Password authentication disabled
- [x] Key-based authentication only
- [x] SSH port protected by firewall

## Regular Maintenance
- [ ] Weekly: Check for failed login attempts
- [ ] Weekly: Review Fail2Ban banned IPs
- [ ] Monthly: Update system packages
- [ ] Monthly: Review Docker container logs
- [ ] Monthly: Check disk space usage

## Security Commands
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Check failed logins
sudo grep "Failed password" /var/log/auth.log | tail -20

# Check Fail2Ban status
sudo fail2ban-client status sshd

# Check disk space
df -h

# Check Docker logs
docker compose logs --tail=100

# Clean up Docker
docker system prune -a
```
EOF

cat ~/security-checklist.md
```

---

## ✅ Server Setup Complete!

Your server is now:
- ✅ Fully updated
- ✅ Secured with firewall (UFW)
- ✅ Protected from brute force (Fail2Ban)
- ✅ SSH hardened (key-only, no root)
- ✅ Docker installed and configured
- ✅ Ready for application deployment

---

## Next Steps

1. **Continue to Application Deployment**
   - See [DEPLOYMENT.md](./DEPLOYMENT.md) Part 6

2. **Set Up Domain**
   - Configure DNS to point to your server
   - See [DEPLOYMENT.md](./DEPLOYMENT.md) Part 7

3. **Deploy Application**
   - Follow deployment steps
   - Configure Caddy for HTTPS
   - Set up Watchtower for auto-updates

---

## Useful Commands Reference

### System Management
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Reboot server
sudo reboot

# Check system resources
htop
df -h
free -h

# Check system logs
sudo journalctl -xe
```

### Firewall Management
```bash
# Check firewall status
sudo ufw status verbose

# Add new rule
sudo ufw allow PORT_NUMBER/tcp

# Delete rule
sudo ufw delete allow PORT_NUMBER/tcp

# Reload firewall
sudo ufw reload
```

### Fail2Ban Management
```bash
# Check status
sudo fail2ban-client status sshd

# Unban IP
sudo fail2ban-client set sshd unbanip IP_ADDRESS

# Restart Fail2Ban
sudo systemctl restart fail2ban
```

### Docker Management
```bash
# Check Docker status
sudo systemctl status docker

# View Docker logs
sudo journalctl -u docker

# Clean up Docker
docker system prune -a

# View resource usage
docker stats
```

---

## Troubleshooting

### Can't Connect via SSH

1. **Check if firewall allows SSH:**
   ```bash
   sudo ufw status | grep 22
   ```

2. **Check SSH service:**
   ```bash
   sudo systemctl status sshd
   ```

3. **Check Fail2Ban:**
   ```bash
   sudo fail2ban-client status sshd
   sudo fail2ban-client set sshd unbanip YOUR_IP
   ```

### Forgot to Allow Port Before Enabling UFW

**If you locked yourself out:**

1. Log into Digital Ocean console (web-based)
2. Click "Access" → "Launch Droplet Console"
3. Log in as root or your user
4. Allow SSH port:
   ```bash
   sudo ufw allow 22/tcp
   ```

### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
exit
ssh yourname@YOUR_SERVER_IP

# Verify
docker ps
```

---

## Additional Resources

- [MyWebClass Hosting Guide](https://github.com/kaw393939/mywebclass_hosting)
- [Digital Ocean Documentation](https://docs.digitalocean.com/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [UFW Documentation](https://help.ubuntu.com/community/UFW)
- [Fail2Ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)

---

**Server setup completed successfully! 🎉**

Continue with [DEPLOYMENT.md](./DEPLOYMENT.md) to deploy your application.
