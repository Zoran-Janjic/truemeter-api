# TrueMeter API - Deployment Guide 🚀

This guide helps you deploy the TrueMeter Fraud Detection API so your Next.js frontend can access it.

## 📦 Prerequisites

- Docker installed
- Git repository (GitHub recommended)
- Account on deployment platform (Railway/Render/DigitalOcean)

---

## 🎯 Quick Deployment Options

### Option 1: Railway (Recommended) ⭐

**Why Railway?**
- Free tier available
- Automatic HTTPS
- Easy GitHub integration
- Zero configuration needed

**Steps:**

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `truemeter-api` repository
   - Railway auto-detects Dockerfile and deploys!

3. **Get your API URL**
   - Click on your deployment
   - Go to "Settings" → "Generate Domain"
   - Copy the URL (e.g., `https://truemeter-api-production.up.railway.app`)

4. **Update CORS in your code** (if needed)
   - Edit `app/config.py`
   - Change `CORS_ORIGINS = ["*"]` to your Next.js domain

5. **Use in Next.js**
   ```typescript
   const API_URL = "https://your-app.up.railway.app";
   
   const response = await fetch(`${API_URL}/api/check`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(carData)
   });
   ```

---

### Option 2: Render

**Steps:**

1. **Push to GitHub** (same as Railway)

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name**: truemeter-api
     - **Environment**: Docker
     - **Region**: Choose closest to your users
     - **Instance Type**: Free

3. **Get URL and use in Next.js**
   - Render provides a URL like `https://truemeter-api.onrender.com`

---

### Option 3: DigitalOcean App Platform

**Steps:**

1. **Create an account** on [DigitalOcean](https://www.digitalocean.com)

2. **Deploy**
   - Go to "Apps" → "Create App"
   - Connect your GitHub repository
   - DigitalOcean detects Dockerfile automatically
   - Choose region and instance size
   - Deploy (~$5/month for basic)

---

## 🧪 Testing Your Deployed API

After deployment, test your endpoints:

```bash
# Health check
curl https://your-api-url.com/health

# Fraud detection
curl -X POST "https://your-api-url.com/api/check" \
  -H "Content-Type: application/json" \
  -d '{
    "make": "BMW",
    "model": "320",
    "year": 2012,
    "reported_km": 15000,
    "fuelType": "Diesel",
    "gearbox": "Automatic",
    "horsepower": 184,
    "price": 9000,
    "offerType": "Used"
  }'
```

---

## 🔗 Connecting to Next.js

### Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-deployed-api.com
```

### API Client (lib/api.ts)
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function checkCarFraud(carData: CarInput) {
  const response = await fetch(`${API_URL}/api/check`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(carData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to check car fraud');
  }
  
  return response.json();
}

export async function checkAPIHealth() {
  const response = await fetch(`${API_URL}/health`);
  return response.json();
}
```

---

## 🔒 Security Best Practices

### Update CORS for Production

Edit `app/config.py`:
```python
# Development
CORS_ORIGINS = ["*"]

# Production
CORS_ORIGINS = [
    "https://your-nextjs-app.vercel.app",
    "https://your-custom-domain.com"
]
```

---

## 📊 API Documentation

Once deployed, visit:
- **Swagger UI**: `https://your-api-url.com/docs`
- **ReDoc**: `https://your-api-url.com/redoc`

---

## 🐳 Local Docker Testing

Before deploying, test locally:

```bash
# Using docker-compose
docker-compose up

# Or manually
docker build -t truemeter-api .
docker run -p 8000:8000 truemeter-api
```

Visit: http://localhost:8000/docs

---

## 🎉 You're Done!

Your API is now:
- ✅ Deployed online
- ✅ Accessible via HTTPS
- ✅ Ready for your Next.js app
- ✅ Auto-scaling and monitored

Need help? Check the deployment platform's documentation or create an issue on GitHub!
