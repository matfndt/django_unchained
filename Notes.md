# Planning to speed-up Django

## Fix the ORM

### What does it do?

- Abstrracts databse operations into python model definitions
- Maps models to databbase tables
- Provides methods for __creating__, __querying__, __updating__ and __deleting__ records

#### Components

- __QuerySets__:
  - A collection of objects from the database
  - Use lazy evaluation (queries aren't executed until explicitly needed)
- __Managers__:
  - Provide interfaces to retrieve and operate on model data.
- __Field Types__:
  - Represent the types and constraints of each column, supporting different databases by adapting SQL syntax

#### Ideas for imporvement

- Optimizing ORM to prefetch related objects when necessary
- Aggreggation functions can slow down queriees if they require full table scans
- make ORM async by default

- SQLx for Database Queries: Directly load data into Polars DataFrames after fetching it with SQLx. By avoiding intermediate Python processing and moving directly from SQL to DataFrame manipulation in Rust, you reduce Python’s role in data manipulation significantly.
- Async and Batched Processing: Use Tokio to handle async queries and enable efficient parallel processing of data batches, especially useful when loading large datasets or performing multiple transformations in sequence.

- Command Interface in Python: Python functions should act primarily as simple orchestration layers, issuing commands to the Rust backend and then receiving the results. This aligns with Python’s strengths in readability and control flow without relying on it for computation.
- Integration with FastAPI for API Layer: If using FastAPI, you can create endpoints that pass parameters directly to Rust for data processing and respond to the user with the results. This keeps Python’s role to a minimum while making the framework accessible through familiar web API calls.

#### Use Protobufs or Arrow

- decide whether to use Protobufs or Arrow

#### Example of how the python side should look like

```python
# Python code (snake_trail) – Minimal computation, primarily orchestration
from rail_forge import fetch_and_aggregate_users

async def get_user_aggregates():
    # Pass parameters to Rust for filtering and aggregation
    result = await fetch_and_aggregate_users(age_range=(20, 30), region="NA")
    # Return processed result directly for frontend or further light processing
    return result
```

Django equivalent

```python
from django.db.models import Count, Avg
from myapp.models import User

def get_user_aggregates():
    # Perform filtering, aggregation, and grouping on the User model
    result = (
        User.objects
        .filter(age__gte=20, age__lte=30, region="NA")  # Filter users by age range and region
        .annotate(average_age=Avg("age"))               # Example aggregate: average age
        .values("average_age")                          # Select only aggregated values
    )
    return result
```
