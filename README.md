# forkcast
A simple FastAPI-based restaurant recommendation system.

# Forkcast 🍽️

**Forkcast** is a FastAPI application that provides personalized and diverse restaurant recommendations. It features a layered architecture (Router → Service → Repository → ORM → Database), custom error handling, and full test coverage.

## Features

- Environment-based configuration via `.env`
- SQLAlchemy 2.0 ORM with typed models
- Repository layer with generic and specialized methods
- Service layer enforcing business rules
- Three recommendation strategies:
  - **Simple**: Top-rated filtering by cuisine
  - **Diverse**: Ensures varied cuisines in recommendations
- Clean API routing using FastAPI routers
- Custom exceptions and global handlers
- CI pipelines for linting and testing on PRs to `main`

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Marc-Xu/forkcast.git
   cd forkcast
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

### Running the App

#### Locally
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```
GET /health
Response: { "status": "ok" }
```

### Restaurants
```
POST   /restaurants/               Create a new restaurant
GET    /restaurants/               List restaurants (skip, limit)
GET    /restaurants/{id}           Retrieve by ID
PATCH  /restaurants/{id}           Partially update
DELETE /restaurants/{id}           Delete by ID
```

### Specialized Recommendations
```
GET /restaurants/top?cuisine=X&n=3
    → Top N restaurants of cuisine X

GET /restaurants/recommend/diverse?n=5
    → N restaurants with maximized cuisine diversity
```

## Testing

Run the full pytest suite:
```bash
pytest --maxfail=1 --disable-warnings -q
```

Tests spin up an in-memory SQLite database per test for isolation.

## CI & Deployment

- **GitHub Actions** workflows in `.github/workflows/`
  - `ci.yml` runs Black, Ruff, and pytest on pull requests.
  - `release.yml` automatically bumps the patch version on `main` merges.
- **Docker** support via the provided `Dockerfile`.

## Contributing

1. Fork the repo and create a feature branch.
2. Write tests for your changes.
3. Ensure linting and tests pass locally.
4. Open a pull request; CI will validate your changes.