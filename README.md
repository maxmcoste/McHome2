# McHome2

McHome2 is a comprehensive Home Temperature Management System built with Python, FastAPI, and PostgreSQL. It allows for monitoring room temperatures, managing smart devices (boilers, valves), and running predictive thermal models to optimize heating schedules.

## Features

- **Room Monitoring**: Track current temperature, humidity, and window status.
- **Device Management**: detailed registry and control for heating hardware.
- **Smart Predictions**: Uses PID controllers and thermal models to predict future temperature trends based on boiler usage and external factors.
- **Flexible Scheduling**: Set target temperatures for different times of the day.
- **Automated Control**: Background tasks automatically adjust the boiler state based on aggregated demand.
- **REST API**: Full-featured API for integrations.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- Alternatively, Python 3.12+ and PostgreSQL 16+ for local development.

## Quick Start (Docker)

The easiest way to run the application is using Docker Compose.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd McHome2
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the frontend and backend images.
   - Start a PostgreSQL database container.
   - Start the main application container.

3. **Access the Application**:
   - **Web Interface**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

   *Note: The first run might take a few moments to initialize the database.*

## Configuration

The application is configured via environment variables. The Docker setup provides sensible defaults in `docker-compose.yml`.

| Variable | Description | Default |
|----------|-------------|---------|
| `MCHOME2_DATABASE_URL` | Database connection string | `postgresql+asyncpg://localhost:5432/mchome2` |
| `MCHOME2_SETTINGS_FILE` | Path to JSON file for dynamic settings | `None` (or `/app/data/settings.json` in Docker) |
| `MCHOME2_SENSOR_POLL_INTERVAL_SECONDS` | How often to poll sensors | `30` |
| `MCHOME2_PREDICTION_INTERVAL_SECONDS` | How often to recalculate heating model | `300` |
| `MCHOME2_PREDICTION_HORIZON_MINUTES` | Forecast duration for thermal model | `240` |
| `MCHOME2_READING_RETENTION_DAYS` | Days to keep sensor history | `90` |
| `MCHOME2_DEFAULT_BOILER_POWER_WATTS` | Power rating of the boiler | `15000.0` |

## Local Development Setup

If you wish to run the application without Docker:

1. **Install Python 3.12+**.

2. **Set up PostgreSQL**:
   - Create a database named `mchome2`.
   - Ensure you have a user with access rights.

3. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

4. **Configure Environment**:
   Export the database URL:
   ```bash
   export MCHOME2_DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mchome2"
   ```

5. **Run Database Migrations**:
   Initialize the database schema using Alembic:
   ```bash
   alembic upgrade head
   ```

6. **Start the Server**:
   ```bash
   uvicorn mchome2.main:app --reload
   ```

## Project Structure

- **`src/`**: Source code for the backend application.
  - **`mchome2/api`**: FastAPI route definitions.
  - **`mchome2/models`**: SQLAlchemy database models.
  - **`mchome2/schemas`**: Pydantic data schemas.
  - **`mchome2/services`**: Business logic.
  - **`mchome2/prediction`**: Thermal modeling and control algorithms.
- **`alembic/`**: Database migration scripts.
- **`frontend/`**: Source code for the web interface.
- **`tests/`**: Pytest test suite.

## Running Tests

To run the test suite:

```bash
pytest
```
