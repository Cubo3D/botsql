# Telegram Bot for General Purposes

This project consists of a Telegram bot for general purposes that is simply configurable, dockerizable, observable, and customizable.

# How to Install?

- Clone this project
```bash
cd your_directory
git clone https://github.com/xvierdev/TelegramBot
cd TelegramBot
```

- Create a `.env` file
```bash
cp .env.example .env
```

- Edit your `.env` file and add your Telegram bot token:
```text
BOT_TOKEN='your-telegram-bot-token-here'
```

## Running with Docker

- Build the Docker image
```bash
docker build -t telegram-bot .
```

- Run the container with your `.env` file
```bash
docker run -d --name telegram-bot --env-file .env telegram-bot
```

- View logs
```bash
docker logs -f telegram-bot
```

- Stop the container
```bash
docker stop telegram-bot
docker rm telegram-bot
```

Enjoy!