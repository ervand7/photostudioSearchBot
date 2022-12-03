Telegram-bot for easy searching rent of photo studios in Moscow. Bot searches on 3 best popular rental sites by parameters: date, time, footage, price, availability of one or another professional equipment for photographers. Stack: Docker, Python, aiogram, selenium, beautifulsoup. Implemented as a microservice.
<br>
Before run: create .env file and set variables:
 - BOT_API_TOKEN=
 - SELENIUM_DRIVER_HOST=
 - SE_NODE_SESSION_TIMEOUT=
 - SE_SESSION_REQUEST_TIMEOUT=
 - SE_NODE_MAX_SESSIONS=
 - SE_NODE_OVERRIDE_MAX_SESSIONS=

Run: `docker-compose up`