#!/usr/bin/env python
"""
Load testing script for the METARing Django application.
This script uses the requests library to simulate real HTTP traffic.
Run with: python load_test.py
"""

import requests
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Configuration
BASE_URL = "http://localhost:8000"  # Adjust if your server runs on different port
ENDPOINTS = {
    'home': '/',
    'airport_detail': '/airport/{icao}/',
    'airport_decoded': '/airport/{icao}/decoded/',
    'airport_compare': '/airport_compare/',
}

# Test airports
TEST_AIRPORTS = [
    'KJFK', 'KLAX', 'KORD', 'KDEN', 'KSFO',
    'LEMD', 'LEBL', 'EGLL', 'EHAM', 'LFPG'
]


class LoadTester:
    def __init__(self, base_url=BASE_URL, num_threads=10, num_requests=100):
        self.base_url = base_url
        self.num_threads = num_threads
        self.num_requests = num_requests
        self.session = requests.Session()
        self.results = []

    def make_request(self, endpoint, **kwargs):
        """Make a single HTTP request and measure response time"""
        start_time = time.time()

        try:
            if endpoint == 'home':
                url = f"{self.base_url}/"
            elif endpoint == 'airport_detail':
                url = f"{self.base_url}/airport/{kwargs['icao']}/"
            elif endpoint == 'airport_decoded':
                url = f"{self.base_url}/airport/{kwargs['icao']}/decoded/"
            elif endpoint == 'airport_compare':
                url = f"{self.base_url}/airport_compare/?icao1={kwargs.get('icao1', 'KJFK')}&icao2={kwargs.get('icao2', 'KLAX')}"
            else:
                return {'error': f'Unknown endpoint: {endpoint}'}

            response = self.session.get(url, timeout=30)
            end_time = time.time()

            return {
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code == 200,
                'url': url
            }

        except requests.exceptions.RequestException as e:
            end_time = time.time()
            return {
                'endpoint': endpoint,
                'status_code': None,
                'response_time': end_time - start_time,
                'success': False,
                'error': str(e)
            }

    def run_load_test(self, test_type='mixed'):
        """Run the load test"""
        print(f"Starting {test_type} load test with {self.num_threads} threads and {self.num_requests} requests...")

        if test_type == 'home':
            requests_list = [{'endpoint': 'home'} for _ in range(self.num_requests)]
        elif test_type == 'airport_detail':
            requests_list = [
                {'endpoint': 'airport_detail', 'icao': airport}
                for airport in TEST_AIRPORTS
                for _ in range(self.num_requests // len(TEST_AIRPORTS))
            ]
        elif test_type == 'airport_decoded':
            requests_list = [
                {'endpoint': 'airport_decoded', 'icao': airport}
                for airport in TEST_AIRPORTS[:5]  # Limit to first 5 for decoded tests
                for _ in range(self.num_requests // 5)
            ]
        elif test_type == 'mixed':
            # Mix of different request types
            requests_list = []
            for _ in range(self.num_requests):
                import random
                if random.random() < 0.3:
                    requests_list.append({'endpoint': 'home'})
                elif random.random() < 0.6:
                    requests_list.append({
                        'endpoint': 'airport_detail',
                        'icao': random.choice(TEST_AIRPORTS)
                    })
                else:
                    requests_list.append({
                        'endpoint': 'airport_decoded',
                        'icao': random.choice(TEST_AIRPORTS[:5])
                    })

        # Execute requests concurrently
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [
                executor.submit(self.make_request, **req)
                for req in requests_list
            ]

            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)

        self.print_results()

    def print_results(self):
        """Print test results"""
        if not self.results:
            print("No results to display")
            return

        successful_requests = [r for r in self.results if r.get('success', False)]
        failed_requests = [r for r in self.results if not r.get('success', False)]

        response_times = [r['response_time'] for r in self.results]

        print("\n" + "="*60)
        print("LOAD TEST RESULTS")
        print("="*60)
        print(f"Total requests: {len(self.results)}")
        print(f"Successful requests: {len(successful_requests)}")
        print(f"Failed requests: {len(failed_requests)}")
        print(".1f")
        print(".1f")
        print(".1f")
        print(".1f")
        print(".1f")

        if failed_requests:
            print(f"\nFailed requests: {len(failed_requests)}")
            for failure in failed_requests[:5]:  # Show first 5 failures
                print(f"  - {failure.get('endpoint', 'unknown')}: {failure.get('error', 'Unknown error')}")

        # Breakdown by endpoint
        print("\nBreakdown by endpoint:")
        endpoints = {}
        for result in self.results:
            endpoint = result.get('endpoint', 'unknown')
            if endpoint not in endpoints:
                endpoints[endpoint] = []
            endpoints[endpoint].append(result)

        for endpoint, results in endpoints.items():
            success_count = sum(1 for r in results if r.get('success', False))
            avg_time = statistics.mean(r['response_time'] for r in results)
            print(f"  {endpoint}: {success_count}/{len(results)} successful, avg {avg_time:.2f}s")


def main():
    parser = argparse.ArgumentParser(description='Load test the METARing application')
    parser.add_argument('--url', default=BASE_URL, help='Base URL of the application')
    parser.add_argument('--threads', type=int, default=10, help='Number of concurrent threads')
    parser.add_argument('--requests', type=int, default=100, help='Total number of requests')
    parser.add_argument('--type', choices=['home', 'airport_detail', 'airport_decoded', 'mixed'],
                       default='mixed', help='Type of load test to run')

    args = parser.parse_args()

    tester = LoadTester(
        base_url=args.url,
        num_threads=args.threads,
        num_requests=args.requests
    )

    try:
        tester.run_load_test(args.type)
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user")
        tester.print_results()


if __name__ == '__main__':
    main()