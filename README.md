# Rwanda GridWatch API

A FastAPI-based system to monitor power outages in Rwanda by analyzing tweets from Rwanda Energy Group (REG) using Natural Language Processing.

## Features

- **Twitter Integration**: Monitors REG's official Twitter account for outage announcements
- **NLP Processing**: Extracts location, outage type, and cause from tweets
- **RESTful API**: Provides endpoints to query outage data
- **SQLite Database**: Stores historical outage data
- **Background Processing**: Syncs data from Twitter in the background
- **Statistics**: Provides outage statistics and analytics

## Installation

1. **Clone the repository** (if using git)
2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Download spaCy language model**:

```bash
python -m spacy download en_core_web_sm
```

4. **Set up Twitter API credentials** (see Configuration section)

## Configuration

### Twitter API Setup

1. Create a Twitter Developer account at [developer.twitter.com](https://developer.twitter.com)
2. Create a new app and generate API keys
3. Configure the API using the `/config/twitter` endpoint or update the config in your code

### Rwanda Energy Group Twitter Handle

Update the `reg_username` variable in the `TwitterClient.fetch_reg_tweets()` method with the correct REG Twitter handle.

## Usage

### Starting the API

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Configuration

- `POST /config/twitter` - Configure Twitter API credentials

#### Data Synchronization

- `POST /outages/sync` - Sync outages from Twitter (background task)

#### Outage Data

- `GET /outages` - Get outages with optional filters
  - Query parameters: `area`, `status`, `outage_type`, `start_date`, `end_date`, `limit`
- `GET /outages/stats` - Get outage statistics
- `GET /outages/areas` - Get list of affected areas
- `POST /outages/manual` - Manually add an outage
- `DELETE /outages/{outage_id}` - Delete an outage

#### Health

- `GET /health` - Health check

### Example Usage

```python
import requests

# Configure Twitter API
config = {
    "bearer_token": "your_bearer_token",
    "consumer_key": "your_consumer_key",
    "consumer_secret": "your_consumer_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
}
requests.post("http://localhost:8000/config/twitter", json=config)

# Sync outages
requests.post("http://localhost:8000/outages/sync")

# Get outages for Kigali
response = requests.get("http://localhost:8000/outages?area=Kigali")
outages = response.json()

# Get statistics
response = requests.get("http://localhost:8000/outages/stats")
stats = response.json()
```

## Data Models

### Outage Model

```python
{
    "id": int,
    "tweet_id": str,
    "area": str,
    "outage_type": "outage" | "restoration" | "maintenance",
    "status": "active" | "resolved" | "scheduled",
    "timestamp": datetime,
    "estimated_duration": str (optional),
    "cause": str (optional),
    "tweet_text": str,
    "confidence": float (0.0-1.0)
}
```

## NLP Processing

The system uses Natural Language Processing to extract information from tweets:

### Location Detection

- Maintains a database of Rwanda districts and sectors
- Uses spaCy Named Entity Recognition for additional location detection

### Outage Classification

- **Outage**: Keywords like "outage", "blackout", "power cut", "no power"
- **Restoration**: Keywords like "restored", "power back", "service resumed"
- **Maintenance**: Keywords like "maintenance", "scheduled", "planned"

### Cause Detection

- **Technical**: Equipment failures, transformer issues, cable faults
- **Weather**: Storm, rain, wind, lightning related
- **Maintenance**: Planned maintenance activities
- **Load**: Overload or high demand situations

## Database Schema

```sql
CREATE TABLE outages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT UNIQUE NOT NULL,
    area TEXT NOT NULL,
    outage_type TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    estimated_duration TEXT,
    cause TEXT,
    tweet_text TEXT NOT NULL,
    confidence REAL NOT NULL,
```
