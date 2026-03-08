# Flexcity Tech Test

## How to Run the Project

### Setup
1. **Install Python 3.14+ and Poetry**
    - `pip install poetry`
2. **Install dependencies**:
   - Use Poetry: `poetry install`
3. **Apply migrations to create and set the database**:
   - `poetry run python manage.py migrate`
4. **(optional) Create superuser account to access admin page**
    - `poetry run python manage.py createsuperuser`
    - Follow the prompts to set up a username and password for the admin account.
5. **(optional) Generate random assets for testing**:
   - `poetry run python manage.py generate_random_assets --count 100`
6. **Run the server**:
   - `poetry run python manage.py runserver`

### Testing
- Use the provided Postman collection to test the API endpoints.
- Access the admin page at http://localhost:8000/admin to manage assets and availabilities
- Curl example to activate assets:
```bash
curl --location 'http://localhost:8000/api/activate?policy=greedy' \
--header 'Content-Type: application/json' \
--data '{
    "date": "2026-03-08",
    "volume": 150
}'
```

## Design Decisions

### Web server

- The project uses Django Ninja for rapid development and ORM capabilities.
- API endpoints and schemas are organized in the `activation` app for modularity.
- An admin page is available at http://localhost:8000/admin to easily add and update assets and availabilities.
- The django command can be used to generate random assets in the database.
- Business logic for asset selection is separated into `greedy.py` and `knapsack_solver.py` for clarity and maintainability.

### Asset Activation Logic

The `strategy.py` module implements a strategy pattern to select the appropriate asset activation algorithm based on configuration.

#### All
`all` selects all activable assets, which is the simplest approach and technically valid, but the worst optization. Used during early development.

#### Greedy
`greedy` is a simple heuristic that sorts assets by cost-effectiveness and selects them until the volume requirement is met. It then removes the least cost-effective assets if the total volume exceeds the requirement. The complexity is O(n^2 log n), which is efficient for moderate numbers of assets.

#### Knapsack Solver
`knapsack_solver` uses a more complex optimization approach to find the best combination of assets within the volume constraint. The problem is modeled as a reversed knapsack problem where we want to minimize the cost while maximizing the volume, and the solver is used to find the assets that are NOT selected, which are then removed from the activable assets. 

The complexity of the knapsack solver is generally _O(n.W)_ where n is the number of assets and W is the volume requirement, which can be more efficient than the greedy approach for larger datasets. In our case, since we reversed the problem, the complexity is _O(n.(maxW - W))_ where maxW is the maximum available volume, which makes the algorithm more efficient for requirements closer to the maximum available volume.

The solver itself is imported from `ortools`, developed by Google under Apache 2.0 License, which is a powerful optimization library.
Source: https://developers.google.com/optimization/pack/knapsack and https://pypi.org/project/ortools/

### Manual Testing

- A custom Django management command is provided to generate random assets with varying volumes and activation costs for testing purposes. This allows for easy population of the database with realistic test data.
- The generated assets have volumes between 1 and 100 (as integer) and activation costs between 1 and 20 times the volume (as float with 3 digits of precision) to provide a wide range of test scenarios.
- A `/available-assets/` endpoint is available to retrieve the list of activable assets for a given date and volume requirement, which can be used to verify the correctness of the asset selection logic.
- The admin interface allows for manual activation of assets for specific dates, which can be used to test the availability logic and ensure that only activable assets are considered for activation.
- A Postman collection is included in the project for easy testing of the API endpoints

## Assumptions

- Orders of magnitude for asset volumes and activation costs are not specified, so the algorithms are designed to handle a reasonable range of values.

- The greedy approach is fast and simple but may not always yield the optimal solution for asset allocation.
- Assumes asset volumes and activation costs are positive and valid, activation costs are assumed to be 3 digits of precision (tenth of cents).

- The database is SQLite for simplicity; for production, a more robust DB would be preferable. The Django ORM delegates some of the optimization to the database layer, so a production-grade database would improve performance.