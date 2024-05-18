.PHONY: up down clear bot_info

up:
	 docker-compose up -d --build

down:
	 docker-compose down

clear:
	 docker system prune -a -f

bot_info:
	 docker-compose logs bot
