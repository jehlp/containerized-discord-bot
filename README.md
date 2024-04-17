# Containerized Discord Bot

This is a barebones Discord bot that runs inside a Docker container.

## Setup

### Prerequisites
- Docker installed on your system

### Configuration
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/jehlp/containerized-discord-bot
   ```

2. Navigate to the cloned directory:
   ```bash
   cd containerized-discord-bot
   ```

3. Create a `tokens.env` file in the `conf` directory that looks like:
```
DISCORD_TOKEN=<your-discord-token>

POSTGRES_DB=<your-postgresql-database-name>
POSTGRES_USER=<your-postgresql-database-username>
POSTGRES_PASSWORD=<your-postgresql-database-password>

# Use the above values again in DATABASE_URL
DATABASE_URL=postgresql://<postgres_user>:<postgres_password>@db:5432/<postgres-db>
```

### Building the Container
1. Ensure that `control.sh`is executable:
   ```bash
   chmod +x control.sh
   ```

2. Build the Docker image:
   ```bash
   ./control.sh --start
   ```
3. Clean up:
   ```bash
   ./control.sh --stop
   ```
### Logs
- To check the logs of the running bot:
  ```bash
  docker compose logs -f
  ```