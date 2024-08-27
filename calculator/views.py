from django.shortcuts import render
from django.http import JsonResponse
import requests
from collections import deque
import time

window = deque(maxlen=10)

def fetch_numbers(number_type):
    url_map = {
        'p': 'http://20.244.56.144/test/primes',
        'f': 'http://20.244.56.144/test/fibo',
        'e': 'http://20.244.56.144/test/even',
        'r': 'http://20.244.56.144/test/rand',
    }
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzI0NzM4OTMwLCJpYXQiOjE3MjQ3Mzg2MzAsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImI5NzliNTExLTZkNzEtNDVjYy05MWM4LWE1ODdjZGI1ZjExNSIsInN1YiI6InNrYWxpZGluZGlAZ2l0YW0uaW4ifSwiY29tcGFueU5hbWUiOiJHSVRBTSIsImNsaWVudElEIjoiYjk3OWI1MTEtNmQ3MS00NWNjLTkxYzgtYTU4N2NkYjVmMTE1IiwiY2xpZW50U2VjcmV0IjoiRnptUnpvV0FJYkd5dUJ3SiIsIm93bmVyTmFtZSI6IkthbGlkaW5kaSBTcmVlIEhhcnNoYSBWYXJtYSIsIm93bmVyRW1haWwiOiJza2FsaWRpbmRpQGdpdGFtLmluIiwicm9sbE5vIjoiSFUyMUNTRU4wMzAwMzM5In0.YhUIZW6EilUU7BT2PmKh-R41_Fl8e2a08S9k7cg_uO0'  # Replace with your new token
    }
    try:
        response = requests.get(url_map[number_type], headers=headers, timeout=0.5)
        response.raise_for_status()  
        numbers = response.json().get('numbers', [])
        print(f"Fetched numbers for {number_type}: {numbers}") 
        return numbers
    except requests.exceptions.Timeout:
        print("Request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def calculate_average(request, number_type):
    if number_type not in ['p', 'f', 'e', 'r']:
        return JsonResponse({"error": "Invalid number type"}, status=400)

    start_time = time.time()

   
    new_numbers = fetch_numbers(number_type)
    unique_new_numbers = list(set(new_numbers))  


    global window
    previous_window_state = list(window)
    window.extend(unique_new_numbers)

    average = sum(window) / len(window) if window else 0

    response_data = {
        "numbers": unique_new_numbers,
        "windowPrevState": previous_window_state,
        "windowCurrState": list(window),
        "avg": round(average, 2)
    }

    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        print("Response time exceeded 500 ms")
        return JsonResponse({"error": "Response time exceeded"}, status=500)

    return JsonResponse(response_data)
