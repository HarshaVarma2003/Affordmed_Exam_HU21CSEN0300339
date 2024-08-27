from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import requests
from collections import deque
import time

# Create a sliding window to store numbers
window = deque(maxlen=10)

def fetch_numbers(number_type):
    url_map = {
        'p': 'http://20.244.56.144/test/primes',
        'f': 'http://20.244.56.144/test/fibo',
        'e': 'http://20.244.56.144/test/even',
        'r': 'http://20.244.56.144/test/rand',
    }
    response = requests.get(url_map[number_type], timeout=0.5)
    if response.status_code == 200:
        return response.json().get('numbers', [])
    return []

def calculate_average(request, number_type):
    if number_type not in ['p', 'f', 'e', 'r']:
        return JsonResponse({"error": "Invalid number type"}, status=400)

    start_time = time.time()

    new_numbers = fetch_numbers(number_type)
    unique_new_numbers = list(set(new_numbers))

    # Append to window and ensure it's unique and sorted
    global window
    window.extend(unique_new_numbers)

    # Calculate average
    average = sum(window) / len(window) if window else 0

    # Prepare the response
    response_data = {
        "numbers": unique_new_numbers,
        "windowPrevState": list(window)[:-len(unique_new_numbers)] if unique_new_numbers else [],
        "windowCurrState": list(window),
        "avg": round(average, 2)
    }

    # Ensure response time is under 500 ms
    if time.time() - start_time > 0.5:
        return JsonResponse({"error": "Response time exceeded"}, status=500)

    return JsonResponse(response_data)
