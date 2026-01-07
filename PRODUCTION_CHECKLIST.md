# ✅ Production Deployment Checklist

## Before Deploying

### Security
- [ ] Generate new `SECRET_KEY` for production (don't use dev key!)
- [ ] Remove any hardcoded API keys from code
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Review CORS settings (limit allowed origins)

### Database
- [ ] Switch from SQLite to PostgreSQL
- [ ] Backup your development database if needed
- [ ] Test database migrations
- [ ] Set up database backups (if using managed DB)

### Configuration
- [ ] Update `FRONTEND_URL` to your production domain
- [ ] Update `DATABASE_URL` to production database
- [ ] Set `DEBUG=False` or remove debug mode
- [ ] Configure proper logging

### Code
- [ ] Remove debug print statements
- [ ] Remove test files
- [ ] Ensure `requirements.txt` is complete
- [ ] Test all endpoints work
- [ ] Verify frontend loads correctly

### Dependencies
- [ ] All packages in `requirements.txt`
- [ ] No local/development-only packages
- [ ] Python version specified (if needed)

### Testing
- [ ] Test registration/login
- [ ] Test creating bounties
- [ ] Test API endpoints
- [ ] Test frontend UI loads
- [ ] Test on mobile devices

## After Deploying

- [ ] Verify app is accessible
- [ ] Test all major features
- [ ] Check error logs
- [ ] Monitor performance
- [ ] Set up error tracking (optional)
- [ ] Configure custom domain (optional)

## Quick Commands

### Generate Production Secret Key:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Test Production API:
```bash
curl https://your-app.onrender.com/health
```

### Check Logs:
- Render: Dashboard → Your Service → Logs
- Railway: Dashboard → Your Service → Deployments → View Logs

---

## Recommended: Start with Render.com

**Why Render?**
- ✅ Easiest setup
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ PostgreSQL included
- ✅ Auto-deploys from GitHub

**Time to deploy:** ~15 minutes

**Cost:** Free (with limitations) or $7/month for always-on

