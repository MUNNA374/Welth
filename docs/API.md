# API Specification

All endpoints are prefixed with `/api/v1`. State mutation requests require valid headers (`Authorization` and `X-CSRF-Token` cookie match).

## Authentication

### `POST /auth/register`
Creates a new user profile and generates default settings.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123",
    "firstName": "Alex",
    "lastName": "Finance"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid-12345",
    "email": "user@example.com",
    "message": "User registered successfully"
  }
  ```

### `POST /auth/login`
Authenticates a user and returns a JWT access token.
- **Request (Form Data)**:
  - `username`: Email address
  - `password`: Password
- **Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

### `GET /auth/me`
Retrieves current user details. Requires `Authorization: Bearer <token>`.
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-12345",
    "email": "user@example.com",
    "firstName": "Alex",
    "lastName": "Finance",
    "role": "USER"
  }
  ```

## Transactions

### `GET /transactions/`
Lists all transactions for the authenticated user.
- **Response**: `200 OK` list of Transaction items.

### `POST /transactions/`
Adds a transaction. AI auto-categorizes description if category is empty.
- **Request Body**:
  ```json
  {
    "accountId": "uuid-account-123",
    "amount": 42.50,
    "currency": "USD",
    "category": "FOOD",
    "description": "Starbucks Coffee",
    "type": "OUTFLOW"
  }
  ```

### `POST /transactions/upload-receipt`
Uploads a file image, runs Gemini multimodal OCR parsing, saves transaction, and returns details.
- **Request**: Multipart file.
