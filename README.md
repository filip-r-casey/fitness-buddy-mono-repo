# Fitness Buddy Project Breakdown

## Rubric

| Task | A level work (3) | B level work (4) | C level work (7) | Implementation Location |
|------|------------------|------------------|------------------|-------------------------|
| Web application basic form, reporting |  |  | ✅ |[Website](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Data collection |  |  | ✅ |[In App](https://main.d3o1p76xpmptqf.amplifyapp.com/) [Folder](https://github.com/filip-r-casey/fitness-buddy-mono-repo/tree/main/datacollector)|
| Data analyzer |  |  | ✅ |[In App](https://main.d3o1p76xpmptqf.amplifyapp.com/) [Folder](https://github.com/filip-r-casey/fitness-buddy-mono-repo/tree/main/dataanalyzer)|
| Unit tests |  |  | ✅ |[File](https://github.com/filip-r-casey/fitness-buddy-mono-repo/blob/main/tests/test_unit.py#L20)|
| Data persistence any data store |  |  | ✅ |[Website](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Rest collaboration internal or API endpoint |  |  | ✅ |[Website](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Product environment |  |  | ✅ |[Website](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Integration tests |  | ✅ |  | [File](https://github.com/filip-r-casey/fitness-buddy-mono-repo/blob/main/tests/Second%20Integration%20Test.py#8) |
| Using mock objects or any test doubles |  | ✅ | | https://github.com/filip-r-casey/fitness-buddy-mono-repo/blob/main/tests/test_doubles.py#23 |
| Continuous integration |  | ✅ |  |[Website](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Production monitoring instrumenting |  | ✅ |  |
| Continuous delivery | ✅ |  |  |[Deployment](https://main.d3o1p76xpmptqf.amplifyapp.com/)|
| Acceptance tests |  |  |  |
| Event collaboration messaging | ✅ |  |  |

## Architecture

![Architecture](https://fbrepo-static.s3.amazonaws.com/architecture.png)

## Implementations

### Web application basic form, reporting

ReactJS web app hosted at: [Front
End](https://main.d3o1p76xpmptqf.amplifyapp.com/). Code can be found in the
`frontend` directory. This is served from the database through our backend flask
application hosted on Elastic Beanstalk. The code for our backend can be found
in the `backend` directory.
![FrontEnd](https://fbrepo-static.s3.amazonaws.com/frontend.png)

### Data collection

Lambda function that runs every day collecting data from an external API and
sends it to our database. Code for this is located in the `datacollector`
directory.

### Data Analyzer

Flask app hosted on elastic beanstalk that is always listening for changes in
the `progress` table of our database. It takes these new entries and analyzes
them, updating average scores and determing which workouts were record-breaking.
The code for this is located in `dataanalyzer`

### Unit Tests

### Data Persistence

Data is persisted in a PostgreSQL database hosted in Amazon's RDS.

### Rest collaboration

Both the frontend and data analyzer interact with REST applications. The
external workout API is a REST API, and the backend that serves content from the
database is also REST. Here's a basic endpoint from our backend (`backend/app/views.py`)

```python
@app_routes.route('/workouts', methods=['GET'])
def workouts():
    # does this need to be dynamically imported? 
    import psycopg2
    from psycopg2.extras import RealDictCursor
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(**params)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        sql = ("SELECT * "
               "FROM workouts "
               "WHERE name ILIKE %s")
        search = "%" + request.args.get("name", None) + "%"
        cur.execute(sql, (search,))
        results = cur.fetchall()
    return results
```

### Product Environment

All the services used in this application are hosted in AWS.

#### VPC

Used to coordinate networking features between services

#### Elastic Beanstalk

Used to host the backend and data analyzer

#### Lambda

Used to run the data collector

#### Amplify

Used to host the front-end application

### Integration Tests
Two integration tests were written to ensure that we get full points for this section. The first test, api_client_integration, tests to make sure that the api from our 
local end can be accepted remotely, and then issue a statement back to local. The second test file, "Second Integration Test" works in a similar manner, but asserts that the 
fitness buddy app launched with status code 200. 

### Mock Objects/Test Doubles

### Continuous Integration

Continuous Integration in the front-end is handled by AWS Amplify which links to
the repository and automatically adjusts environment variables for production
whenever there is a push. For the rest of the services, it is handled by Github
Actions, and each of them have a slightly different protocol, these are all
described in the `.yml` files in the `.github/workflows` directory.

### Production Monitoring

This is handled by AWS CloudWatch which provides us with logs, service
health, and user metrics.

### Continuous Delivery

This is also in part managed by Github Actions which is responsible for
deploying the applications. On top of this, we have multiple environments in AWS
where we can promote applications from staging to prod within the console itself.

### Acceptance Tests

### Messaging
1. **Event Messaging API**: Introduced new backend endpoints for posting and retrieving messages tied to specific events, enhancing real-time communication capabilities.

2. **React Messaging Components**: Developed `MessageDisplay` and `MessageInput` components in the frontend to display messages and enable message posting, improving user interaction within events.

3. **Integrated Messaging Interface**: Implemented a new `EventPage` that combines display and input components for a seamless event communication experience, fostering better user engagement and collaboration.
