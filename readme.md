# Flask sample project

## How to install?

### Manual install

 1. Clone this project to your local machine
 2. Create conda env from `environment.yml` file
 3. Create postgres database manually. You should create 2 database, 1 for dev and 1 for test purpose
 4. Copy `.env-dev` as `.env`
 5. Configure your database both for dev and test purpose in `.env`
 6. Run this following command

```
   make run-migration
   python app.py
```

 7. Run test (Optional)

```
   make run-test_api
```

### Docker install

1. Make sure you have install both docker and docker compose in your machine
2. Normal run, for dev purpose

```
docker compose -f docker-compose.dev.yml up --build
```

3. Or running in background

```
docker compose -f docker-compose.dev.yml up --build -d
```
