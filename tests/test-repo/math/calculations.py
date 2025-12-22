"""Mathematical calculation utilities"""
import math

def calculate_percentage(value, total):
    """Calculate what percentage value is of total"""
    if total == 0:
        return 0
    return (value / total) * 100

def compound_interest(principal, rate, time, compounds_per_year=12):
    """Calculate compound interest"""
    rate_decimal = rate / 100
    amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * time)
    interest = amount - principal
    
    return {
        'principal': principal,
        'total_amount': round(amount, 2),
        'interest_earned': round(interest, 2)
    }

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    x1, y1 = point1
    x2, y2 = point2
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def factorial(n):
    """Calculate factorial of n"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

def fibonacci(n):
    """Generate fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    
    return True

def greatest_common_divisor(a, b):
    """Calculate GCD using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def least_common_multiple(a, b):
    """Calculate LCM of two numbers"""
    return abs(a * b) // greatest_common_divisor(a, b)

def calculate_statistics(numbers):
    """Calculate mean, median, and mode of a list"""
    if not numbers:
        return None
    
    # Mean
    mean = sum(numbers) / len(numbers)
    
    # Median
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # Mode
    from collections import Counter
    count = Counter(numbers)
    mode = count.most_common(1)[0][0]
    
    return {
        'mean': mean,
        'median': median,
        'mode': mode,
        'min': min(numbers),
        'max': max(numbers)
    }
