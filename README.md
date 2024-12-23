## Run Test

# Run all tests in the project
```bash
docker compose exec web pytest -v
```

# Run tests with reused database (faster)
```bash
docker compose exec web pytest -v --reuse-db
```

# Force database recreation
```bash
docker compose exec web pytest -v --reuse-db --create-db
```

# Run all tests with coverage report
```bash
docker compose exec web pytest -v --cov
```

# Run all tests with detailed HTML coverage report
```bash
docker compose exec web pytest -v --cov --cov-report=html
```

# Run specific app tests
```bash
docker compose exec web pytest apps/listings/tests.py -v
```

# Run specific test cases
```bash
docker compose exec web pytest apps/listings/tests.py -m edit_listing -v
```

# Run with print output
```bash
docker compose exec web pytest apps/listings/tests.py -v -k "edit" -s
```

# Run specific tests with coverage
```bash
docker compose exec web pytest apps/listings/tests.py -v -k "edit" --cov=apps.listings
```


```
docker compose exec web pytest apps/listings/tests.py -v -k "TestOrders"
```


```
ssh-keygen -t ed25519 -C "your_email@example.com" -f $(pwd)/deployment/id_ed25519
```
