# Melodiary setup guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- AWS Account
- Spotify Developer Account

## Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/melodiary.git
cd melodiary
```

## Step 2: Spotify Developer Setup

1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Note your Client ID and Client Secret
4. Add redirect URIs:
   - `http://localhost:5173/callback/spotify` (development)
   - `https://melodiary.io/callback/spotify` (production)

## Step 3: AWS Setup

1. Create DynamoDB tables (see infrastructure/dynamodb_tables.json)
2. Create IAM role for Lambda with DynamoDB access
3. Note your AWS region

## Step 4: Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

## Step 5: Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your API URL and Spotify Client ID
npm run dev
```

## Step 6: Deploy

See deployment instructions in each README.
