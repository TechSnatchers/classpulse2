# Domain Configuration

## Custom Domain

**Domain:** `zoomlearningapp.de`

## URLs

### Production URLs
- **API Base URL:** `https://zoomlearningapp.de`
- **Health Check:** `https://zoomlearningapp.de/health`
- **Zoom Webhook:** `https://zoomlearningapp.de/api/zoom/webhook`
- **Zoom Chatbot:** `https://zoomlearningapp.de/api/zoom/chatbot`

### CloudFront Distribution
- **CloudFront URL:** `https://d1bj83s472gkb2.cloudfront.net`
- **Distribution Name:** `learning-platform-api-cloudfront`

## DNS Configuration

### CNAME Records (in Spaceship DNS)
1. **Main Domain (points to CloudFront):**
   - Type: CNAME
   - Name: `@` (or blank)
   - Value: `d1bj83s472gkb2.cloudfront.net`

2. **WWW Subdomain (optional):**
   - Type: CNAME
   - Name: `www`
   - Value: `d1bj83s472gkb2.cloudfront.net`

## SSL Certificate

- **Certificate ID:** `c66bef06-af85-4122-9fe9-9b48469d31f0`
- **Status:** Pending validation / Issued
- **Domains:** 
  - `zoomlearningapp.de`
  - `*.zoomlearningapp.de` (wildcard)
- **Provider:** AWS Certificate Manager (ACM)
- **Region:** eu-north-1

## Zoom Integration

### Zoom App Configuration
- **Home URL:** `https://zoomlearningapp.de`
- **Domain Allow List:** `zoomlearningapp.de`
- **Bot Endpoint URL:** `https://zoomlearningapp.de/api/zoom/chatbot`
- **Trust Domain List:** `zoomlearningapp.de` (pending approval)

## Environment Variables

Add these to your `.env` file:

```env
# Domain Configuration
DOMAIN=zoomlearningapp.de
BASE_URL=https://zoomlearningapp.de
CLOUDFRONT_URL=https://d1bj83s472gkb2.cloudfront.net

# Zoom Configuration
ZOOM_WEBHOOK_URL=https://zoomlearningapp.de/api/zoom/webhook
ZOOM_CHATBOT_URL=https://zoomlearningapp.de/api/zoom/chatbot
```

## Testing

### Test Domain
```bash
# Health check
curl https://zoomlearningapp.de/health

# API root
curl https://zoomlearningapp.de/

# Chatbot endpoint
curl https://zoomlearningapp.de/api/zoom/chatbot/health
```

## Notes

- Domain is registered with Spaceship
- DNS is managed in Spaceship
- SSL certificate is managed in AWS Certificate Manager
- CloudFront distribution handles HTTPS and caching
- Security headers are configured for Zoom compatibility

