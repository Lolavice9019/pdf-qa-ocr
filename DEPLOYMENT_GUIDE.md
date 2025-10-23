# 🚀 Permanent Deployment Guide

## Quick Deploy Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Best for:** Easy, free, permanent hosting with automatic updates

**Steps:**

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Click "Sign up" or "Sign in with GitHub"

2. **Connect Your GitHub Repository**
   - The repository is already created: `https://github.com/Lolavice9019/pdf-qa-ocr`
   - Click "New app"
   - Select repository: `Lolavice9019/pdf-qa-ocr`
   - Branch: `master`
   - Main file path: `app.py`

3. **Add Secrets (Important!)**
   - Click "Advanced settings"
   - Add your OpenAI API key in secrets:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

4. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes for build
   - You'll get a permanent URL like: `https://your-app-name.streamlit.app`

**Pros:**
- ✅ Completely free
- ✅ Automatic updates when you push to GitHub
- ✅ Custom domain support
- ✅ SSL certificate included
- ✅ No server management needed

---

### Option 2: Heroku (FREE tier available)

**Best for:** More control, custom domain

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # On Ubuntu/Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   
   # On Mac
   brew tap heroku/brew && brew install heroku
   
   # On Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd /path/to/pdf_qa_app
   heroku create your-app-name
   ```

4. **Add Buildpack**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key-here
   ```

6. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

7. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku master
   ```

8. **Open Your App**
   ```bash
   heroku open
   ```

**Your URL:** `https://your-app-name.herokuapp.com`

---

### Option 3: Railway (Modern, Easy)

**Best for:** Modern deployment, generous free tier

**Steps:**

1. **Go to Railway**
   - Visit: https://railway.app/
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `Lolavice9019/pdf-qa-ocr`

3. **Add Environment Variables**
   - Go to Variables tab
   - Add: `OPENAI_API_KEY = your-api-key-here`

4. **Deploy**
   - Railway auto-detects Streamlit
   - Deployment starts automatically
   - Get permanent URL

**Pros:**
- ✅ $5/month free credit
- ✅ Very fast deployment
- ✅ Great developer experience

---

### Option 4: Google Cloud Run (Scalable)

**Best for:** Production apps, high traffic

**Steps:**

1. **Install Google Cloud SDK**
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   ENV PORT=8080
   
   CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Build and Deploy**
   ```bash
   gcloud run deploy pdf-qa-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-api-key-here
   ```

4. **Get URL**
   - Cloud Run provides a permanent HTTPS URL

**Pros:**
- ✅ Pay only for what you use
- ✅ Auto-scaling
- ✅ Very reliable

---

### Option 5: AWS EC2 (Full Control)

**Best for:** Maximum control, custom configuration

**Steps:**

1. **Launch EC2 Instance**
   - Go to AWS Console
   - Launch Ubuntu 22.04 instance
   - Open ports 80 and 443

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx -y
   pip3 install -r requirements.txt
   ```

4. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/streamlit.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Streamlit App
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/pdf_qa_app
   Environment="OPENAI_API_KEY=your-api-key-here"
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   ```

6. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/streamlit
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

7. **Enable and Restart Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

8. **Add SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🎯 Recommended: Streamlit Cloud

For your use case, I **highly recommend Streamlit Cloud** because:

1. ✅ **Completely Free** - No credit card required
2. ✅ **Zero Configuration** - Works out of the box
3. ✅ **Auto-Deploy** - Updates automatically from GitHub
4. ✅ **Professional URL** - Get `your-app.streamlit.app`
5. ✅ **No Maintenance** - Streamlit handles everything

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- ✅ GitHub repository is public or you have Streamlit Cloud access
- ✅ `requirements.txt` is up to date
- ✅ OpenAI API key is ready
- ✅ All files are committed to GitHub
- ✅ App runs locally without errors

---

## 🔐 Security Notes

**Important:** Never commit API keys to GitHub!

**For Streamlit Cloud:**
- Use the Secrets management in settings
- Add: `OPENAI_API_KEY = "your-key"`

**For other platforms:**
- Use environment variables
- Never hardcode keys in code

---

## 🌐 Custom Domain (Optional)

**For Streamlit Cloud:**
1. Go to app settings
2. Click "Custom domain"
3. Add your domain (e.g., `docs.yourdomain.com`)
4. Update DNS records as instructed

**For other platforms:**
- Each platform has domain configuration in settings
- Usually requires updating DNS CNAME or A records

---

## 📊 Monitoring & Logs

**Streamlit Cloud:**
- View logs in the app dashboard
- Monitor usage and errors

**Heroku:**
```bash
heroku logs --tail
```

**Railway:**
- View logs in the Deployments tab

**Google Cloud Run:**
```bash
gcloud run services logs read pdf-qa-app
```

---

## 🔄 Updating Your Deployed App

**Streamlit Cloud / Railway:**
- Just push to GitHub
- Auto-deploys automatically

**Heroku:**
```bash
git push heroku master
```

**Google Cloud Run:**
```bash
gcloud run deploy pdf-qa-app --source .
```

**AWS EC2:**
```bash
ssh into instance
cd /home/ubuntu/pdf_qa_app
git pull
sudo systemctl restart streamlit
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| **Streamlit Cloud** | ✅ Unlimited (public apps) | $0/month |
| **Railway** | $5/month credit | $5+/month |
| **Heroku** | 550 hours/month | $7+/month |
| **Google Cloud Run** | 2M requests/month | Pay per use |
| **AWS EC2** | 750 hours/month (1 year) | $5+/month |

---

## 🆘 Troubleshooting

**App won't start:**
- Check logs for errors
- Verify all dependencies in requirements.txt
- Ensure Python version compatibility

**API key not working:**
- Check environment variable name
- Verify key is correctly set in secrets/config
- Test key locally first

**Slow performance:**
- Consider upgrading to paid tier
- Optimize code (reduce OCR processing)
- Use caching more aggressively

**Out of memory:**
- Reduce file size limits
- Process files in smaller batches
- Upgrade to larger instance

---

## 📞 Support

**Streamlit Cloud Issues:**
- Forum: https://discuss.streamlit.io/
- Docs: https://docs.streamlit.io/streamlit-community-cloud

**General Questions:**
- GitHub Issues: https://github.com/Lolavice9019/pdf-qa-ocr/issues

---

## ✅ Quick Start (Streamlit Cloud)

**5-Minute Deployment:**

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Repository: `Lolavice9019/pdf-qa-ocr`
5. Branch: `master`
6. Main file: `app.py`
7. Advanced settings → Add secret: `OPENAI_API_KEY`
8. Click "Deploy"
9. Done! 🎉

Your app will be live at: `https://[your-app-name].streamlit.app`

---

**Ready to deploy? Start with Streamlit Cloud - it's the easiest option!** 🚀

