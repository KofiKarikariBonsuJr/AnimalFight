# ✅ YOUR ACTION CHECKLIST

Use this checklist to complete your deployment. Check off each item as you complete it.

## Phase 1: Preparation (15 minutes)

### Docker Hub Setup
- [ ] Go to https://hub.docker.com/signup
- [ ] Create account (write down username: _______________)
- [ ] Log in → Account Settings → Security
- [ ] Create "New Access Token"
  - Name: `GitHub Actions CI/CD`
  - Permissions: Read, Write, Delete
- [ ] Copy token (save it temporarily: _______________)

### GitHub Secrets
- [ ] Go to https://github.com/Zoubaiir/project14/settings/secrets/actions
- [ ] Click "New repository secret"
- [ ] Add Secret 1:
  - Name: `DOCKER_USERNAME`
  - Value: (your Docker Hub username)
- [ ] Add Secret 2:
  - Name: `DOCKER_PASSWORD`
  - Value: (your Docker Hub token)

### Update README
```powershell
cd c:\Users\zouba\project14\project14
rm README.md
mv README_NEW.md README.md
```
- [ ] README updated

## Phase 2: Commit & Deploy Code (5 minutes)

### Git Commit
```powershell
cd c:\Users\zouba\project14\project14
git add .
git commit -m "Add production deployment configuration"
git push origin main
```
- [ ] Changes committed
- [ ] Changes pushed to GitHub

### Verify GitHub Actions
- [ ] Go to https://github.com/Zoubaiir/project14/actions
- [ ] Watch workflow run
- [ ] Tests pass ✅
- [ ] Build completes ✅
- [ ] Image pushes to Docker Hub ✅

### Verify Docker Hub
- [ ] Go to https://hub.docker.com/r/YOUR_USERNAME/project14
- [ ] Image `latest` exists
- [ ] Image `main-XXXXXX` exists

## Phase 3: Account Setup (15 minutes)

### GitHub Student Developer Pack (Optional but Recommended)
- [ ] Go to https://education.github.com/pack
- [ ] Apply with student email
- [ ] Get approved (may take 1-2 days)
- [ ] Get $200 Digital Ocean credit
- [ ] Get free Namecheap .me domain

### Digital Ocean Account
- [ ] Go to https://www.digitalocean.com/
- [ ] Sign up (use GitHub Student Pack if available)
- [ ] Add payment method or apply credit
- [ ] Account ready

### Domain Name (Optional but Recommended)
**Option A: GitHub Student Pack**
- [ ] Claim Namecheap domain from student pack
- [ ] Choose domain name: _______________

**Option B: Purchase**
- [ ] Buy from Namecheap, Google Domains, etc.
- [ ] Domain name: _______________

## Phase 4: Server Creation (20 minutes)

### Create Droplet
- [ ] Digital Ocean → Create → Droplets
- [ ] Choose image: **Ubuntu 24.04 (LTS) x64**
- [ ] Choose plan: **Basic $7/month (1GB RAM)**
- [ ] Choose datacenter: (closest to you)
- [ ] Choose SSH key authentication
- [ ] Hostname: `project14-prod`
- [ ] Create Droplet
- [ ] Copy server IP: _______________

### First Connection
```bash
ssh root@YOUR_SERVER_IP
```
- [ ] Connected successfully
- [ ] Server prompt shows: `root@project14-prod:~#`

## Phase 5: Server Security (45 minutes)

Follow **SERVER_SETUP.md** for detailed steps:

### System Updates
```bash
apt update && apt upgrade -y
apt install -y curl wget git ufw fail2ban unattended-upgrades
```
- [ ] System updated
- [ ] Tools installed

### Create Non-Root User
```bash
adduser yourname
usermod -aG sudo yourname
mkdir -p /home/yourname/.ssh
cp /root/.ssh/authorized_keys /home/yourname/.ssh/
chown -R yourname:yourname /home/yourname/.ssh
chmod 700 /home/yourname/.ssh
chmod 600 /home/yourname/.ssh/authorized_keys
```
- [ ] User created: _______________
- [ ] User added to sudo group
- [ ] SSH keys copied

### Test New User
**Open NEW terminal (keep root open):**
```bash
ssh yourname@YOUR_SERVER_IP
sudo apt update
```
- [ ] Connection works
- [ ] Sudo works

### Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp
sudo ufw --force enable
sudo ufw status
```
- [ ] SSH allowed (22)
- [ ] HTTP allowed (80)
- [ ] HTTPS allowed (443)
- [ ] Firewall enabled

### Configure Fail2Ban
```bash
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
sudo fail2ban-client status
```
- [ ] Fail2Ban started
- [ ] Fail2Ban enabled
- [ ] Status shows active

### Harden SSH
```bash
sudo nano /etc/ssh/sshd_config
```
Change:
- `PermitRootLogin no`
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`

```bash
sudo systemctl restart sshd
```
- [ ] SSH config updated
- [ ] SSH restarted
- [ ] Can still connect as user
- [ ] Cannot connect as root

### Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
exit
ssh yourname@YOUR_SERVER_IP
docker --version
```
- [ ] Docker installed
- [ ] User added to docker group
- [ ] Docker version shows

## Phase 6: Deploy Application (30 minutes)

### Create Application Directory
```bash
mkdir -p ~/project14
cd ~/project14
```
- [ ] Directory created

### Create .env File
```bash
nano .env
```

Copy from `.env.example` and update:
- [ ] `DOCKER_USERNAME=` (your Docker Hub username)
- [ ] `DATABASE_URL=` (set strong password)
- [ ] `POSTGRES_PASSWORD=` (same strong password)
- [ ] `JWT_SECRET_KEY=` (generate: `openssl rand -hex 32`)
- [ ] `JWT_REFRESH_SECRET_KEY=` (generate: `openssl rand -hex 32`)
- [ ] `PGADMIN_DEFAULT_PASSWORD=` (set strong password)
- [ ] All other required variables set

### Generate Secrets
```bash
openssl rand -hex 32  # Copy for JWT_SECRET_KEY
openssl rand -hex 32  # Copy for JWT_REFRESH_SECRET_KEY
```
- [ ] JWT secrets generated
- [ ] Added to .env

### Download Configuration Files
```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/Zoubaiir/project14/main/docker-compose.prod.yml
curl -o Caddyfile https://raw.githubusercontent.com/Zoubaiir/project14/main/Caddyfile
```
- [ ] docker-compose.yml downloaded
- [ ] Caddyfile downloaded

### Start Services
```bash
docker compose pull
docker compose up -d
docker compose ps
```
- [ ] Images pulled
- [ ] Services started
- [ ] All containers show "Up" and "healthy"

### Verify Application
```bash
curl http://localhost:8000/health
```
- [ ] Returns: `{"status":"healthy"}`

### Check Logs
```bash
docker compose logs -f web
# Press Ctrl+C to exit
```
- [ ] No errors in logs
- [ ] Application started successfully

## Phase 7: Domain & HTTPS (30 minutes)

### Configure DNS
In your domain registrar:
- [ ] Add A record: `@` → `YOUR_SERVER_IP`
- [ ] Add A record: `www` → `YOUR_SERVER_IP`
- [ ] Wait for DNS propagation (5-60 minutes)

### Verify DNS
```bash
nslookup your-domain.com
```
- [ ] Shows your server IP

### Update Server Configuration
```bash
cd ~/project14
nano .env
```
Update:
- [ ] `DOMAIN=your-actual-domain.com`
- [ ] `EMAIL=your-email@example.com`

### Restart Services
```bash
docker compose down
docker compose up -d
```
- [ ] Services restarted

### Watch Certificate Generation
```bash
docker compose logs -f caddy
```
- [ ] Certificate obtained successfully
- [ ] No errors

### Test HTTPS
- [ ] Open browser to `https://your-domain.com`
- [ ] Site loads successfully
- [ ] Green padlock shows (valid HTTPS)
- [ ] Can register new user
- [ ] Can login
- [ ] Calculator works

## Phase 8: Verify Everything (15 minutes)

### Application Tests
- [ ] Register new user account
- [ ] Login with credentials
- [ ] Create a calculation
- [ ] View calculation history
- [ ] Edit a calculation
- [ ] Delete a calculation
- [ ] Logout and login again

### System Tests
```bash
# Check all containers
docker compose ps
# Should show all healthy

# Check disk space
df -h
# Should have space available

# Check firewall
sudo ufw status
# Should show ports 22, 80, 443

# Check Fail2Ban
sudo fail2ban-client status sshd
# Should show active
```
- [ ] All containers healthy
- [ ] Sufficient disk space
- [ ] Firewall configured
- [ ] Fail2Ban active

### Automatic Deployment Test
1. Make a small change to your app locally
2. Commit and push to GitHub
3. Wait 2-3 minutes for GitHub Actions
4. Wait up to 5 minutes for Watchtower
5. Refresh your website - see the change!

```bash
# Watch the update happen
docker compose logs -f watchtower
```
- [ ] GitHub Actions completed successfully
- [ ] Watchtower detected update
- [ ] New version deployed automatically
- [ ] No downtime observed

## 🎉 Deployment Complete!

### Final Checklist
- [ ] Application accessible at https://your-domain.com
- [ ] HTTPS certificate valid
- [ ] All features working
- [ ] Auto-deployment working
- [ ] Server secured
- [ ] Monitoring set up
- [ ] Documentation reviewed

### Information Summary
Record this for future reference:

- **Server IP**: _______________
- **Domain**: _______________
- **Server User**: _______________
- **Docker Hub**: _______________
- **GitHub Repo**: https://github.com/Zoubaiir/project14

### Credentials to Save Securely
- [ ] SSH private key backed up
- [ ] Server user password saved
- [ ] Database passwords saved (in .env)
- [ ] JWT secrets saved (in .env)
- [ ] PgAdmin password saved (in .env)

### Next Steps
- [ ] Take screenshots for portfolio
- [ ] Write README for resume
- [ ] Document lessons learned
- [ ] Share project on LinkedIn
- [ ] Add to GitHub portfolio

---

## 🆘 Having Issues?

### Quick Troubleshooting

**Can't connect to server:**
- Check firewall: `sudo ufw status`
- Check Fail2Ban: `sudo fail2ban-client status sshd`

**Application not starting:**
- Check logs: `docker compose logs web`
- Verify .env: `cat .env`
- Restart: `docker compose restart web`

**HTTPS not working:**
- Check DNS: `nslookup your-domain.com`
- Check Caddy: `docker compose logs caddy`
- Wait for DNS propagation (can take up to 60 minutes)

**Need detailed help:**
- See DEPLOYMENT.md - Troubleshooting section
- See SERVER_SETUP.md for server issues
- Check mywebclass_hosting guide

---

## 📚 Documentation Quick Links

- **Quick Start**: [QUICKSTART.md](./QUICKSTART.md)
- **Full Deployment**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Server Setup**: [SERVER_SETUP.md](./SERVER_SETUP.md)
- **Implementation Summary**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **Main Guide**: https://github.com/kaw393939/mywebclass_hosting

---

**You've got this! Follow the checklist step by step, and you'll have a production application running in no time.** 🚀

**Estimated Total Time**: 3-4 hours (spread over 1-2 days to allow for DNS propagation)
