# Campaign Targeting Engine

A microservice that routes the right campaigns to the right requests based on targeting criteria.

## Overview

This service provides campaign targeting capabilities through a simple HTTP API. It matches incoming requests with campaigns based on various targeting criteria such as:
- App ID
- Country
- Operating System

## Features

- Campaign management with active/inactive states
- Flexible targeting rules with include/exclude conditions
- SQLite database for easy development (configurable for production)
- RESTful API for campaign delivery
- Comprehensive test coverage

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (copy `.env.example` to `.env` and edit as needed):
```
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
FLASK_APP=app.py
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the development server:
```bash
flask run
```

## API Documentation

### Get Matching Campaign

```http
GET /api/v1/delivery?app_id=com.example.app&country=US&os=android
```

Query Parameters:
- `app_id` (required): The ID of the requesting app
- `country` (required): The country code of the user
- `os` (required): The operating system of the user

Success Response:
```json
{
    "success": true,
    "data": {
        "cid": "campaign_id",
        "img": "https://example.com/image.jpg",
        "cta": "Install Now"
    }
}
```

## Testing

Run the test suite:
```bash
python -m pytest
```

## License

MIT
