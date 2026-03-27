# Load Testing for METARing

This directory contains load testing tools for the METARing Django application.

## Django Unit Load Tests

The `myapp/tests.py` file includes `LoadTest` class with several load testing methods:

- `test_concurrent_home_page_access()` - Tests concurrent access to the home page
- `test_concurrent_airport_detail_access()` - Tests concurrent airport detail page access
- `test_concurrent_airport_decoded_access()` - Tests concurrent decoded airport page access
- `test_mixed_workload_simulation()` - Tests mixed workload with different request types

Run the Django load tests with:
```bash
python manage.py test myapp.tests.LoadTest --verbosity=2
```

## Standalone Load Testing Script

The `load_test.py` script provides comprehensive load testing using the `requests` library to simulate real HTTP traffic.

### Prerequisites

Install the requests library:
```bash
pip install requests
```

### Usage

Start your Django development server first:
```bash
python manage.py runserver
```

Then run the load test in a separate terminal:

```bash
# Basic mixed workload test (default)
python load_test.py

# Test specific endpoint types
python load_test.py --type home
python load_test.py --type airport_detail
python load_test.py --type airport_decoded

# Custom configuration
python load_test.py --threads 20 --requests 500 --url http://localhost:8000

# Full options
python load_test.py --help
```

### Test Types

- **home**: Tests only the home page
- **airport_detail**: Tests airport detail pages for various airports
- **airport_decoded**: Tests decoded METAR pages (more resource-intensive)
- **mixed**: Simulates real user behavior with a mix of all endpoints

### Example Output

```
Starting mixed load test with 10 threads and 100 requests...
============================================================
LOAD TEST RESULTS
============================================================
Total requests: 100
Successful requests: 98
Failed requests: 2
Success rate: 98.0%
Average response time: 0.45s
Median response time: 0.32s
95th percentile: 1.20s
99th percentile: 2.10s
Min response time: 0.08s
Max response time: 3.50s

Breakdown by endpoint:
  home: 28/30 successful, avg 0.15s
  airport_detail: 45/48 successful, avg 0.52s
  airport_decoded: 25/22 successful, avg 0.78s
```

### Interpreting Results

- **Success Rate**: Should be >95% under normal load
- **Response Times**:
  - Home page: <0.5s average
  - Airport detail: <1.0s average
  - Decoded pages: <2.0s average (METAR API dependent)
- **95th/99th Percentiles**: Should be reasonable (<5s for 95th percentile)

### Performance Tuning

If tests show poor performance:
1. Check database connections and query optimization
2. Review METAR API caching strategy
3. Consider adding database indexes
4. Implement proper caching (Redis/Memcached)
5. Use a production WSGI server (gunicorn/uwsgi) instead of runserver

### Load Testing Best Practices

1. Run tests on a staging environment first
2. Gradually increase load (threads/requests)
3. Monitor server resources (CPU, memory, database connections)
4. Test during different times of day
5. Include realistic user behavior patterns
6. Set up proper monitoring and alerting