# JWT Authentication Backend

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation Steps
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL Database
```bash
# Create database
createdb jwt_auth_db

# Update .env file with your database credentials
```

4. Run the application
```bash
flask run
```

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: Secret key for JWT token generation

## API Endpoints
- `POST /api/auth/register`: User registration
- `POST /api/auth/login`: User login
- `GET /api/dashboard`: Protected route (requires JWT token)

## Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- Token expiration
- Input validation