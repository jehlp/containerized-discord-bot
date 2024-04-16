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

3. Modify the `tokens.env` file with your Discord bot token.

### Building the Container
1. Ensure that `control.sh` is executable:
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
  docker logs my-bot
  ```