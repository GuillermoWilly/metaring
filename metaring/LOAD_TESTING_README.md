# Load Testing for METARing

This directory contains load testing tools for the METARing Django application using **Locust**.

---

## Locust Load Testing

The `load_tests.py` file defines a `LoadTestUser` class that simulates different types of user behavior against the application.

### Prerequisites

Install Locust:

```bash
pip install locust

Start your Django server first:

python manage.py runserver

locust -f load_tests.py

'''Open your browser at:

http://localhost:8089

Configure:

Number of users
Spawn rate
Host

Notes

The login system requires a valid user:

username: UsuarioPrueba
password: UsuarioPrueba
Make sure this user exists before running tests.'''