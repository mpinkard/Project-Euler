import math
import copy
from collections import Counter
from itertools import combinations
import numpy as np
import operator


"""
    Returns prime factors of a given non-negative number
"""
def prime_factors(n, primes=[]):
    copied_primes = copy.deepcopy(primes)
    if n < 0:
        raise ValueError('Negative values are not valid')
    if n < 2:
        return copied_primes
    for i in range(2, math.floor(n/2) + 1):
        if n % i == 0:
            copied_primes.append(i)
            return prime_factors(n/i, primes=copied_primes)
    
    copied_primes.append(n)
    return copied_primes

"""
    Returns all divisors of a given number n
"""
def all_divisors(n):
    if n == 0:
        return set([])
    if n < 0:
        prime_divisors = prime_factors(-1 * n)
        divisors = [-1, *prime_divisors]
    else:
        prime_divisors = prime_factors(n)
        divisors = [1, *prime_divisors]
    for i in range(1, len(prime_divisors)+1):
        divisors = [*divisors, *list(map(np.prod, combinations(prime_divisors, i)))]
    return set(divisors)

"""
    Generates the natural numbers:
        1, 2, 3, 4 ...
"""
def natural_number_generator():
    n = 1
    while True:
        yield n
        n += 1

"""
    Generates the triangular numbers: 
        1, 3, 6, 10, 15 ...
    whose n-th element can be arrived at through adding the 
    first n natural numbers:
        t_5 = 1 + 2 + 3 + 4 + 5 = 15
"""
def triangle_number_generator():
    n = natural_number_generator()
    triangle = next(n)
    while True:
        yield triangle
        triangle += next(n)

"""
    Returns the first triangular number with greater-than n divisors

    NOTE: Is currently too slow
"""
def triangle_divisors(n):
    triangle = triangle_number_generator()
    while True:
        t = next(triangle)
        divisors = all_divisors(t)
        if len(divisors) > n:
            return t
"""
    Finds the smallest number that can be divided by all numbers 1 ... n
"""
def smallest_multiple(n):
    if n < 0:
        raise ValueError('Negative values are not valid')
    if n == 0 or n == 1:
        return n
    primes = Counter()
    for i in range(2, n + 1):
        # Does a union: ((2, 2)) U ((2, 3), (3,2)) => ((2, 3), (3, 2))
        # Where the first number is a prime and the second is the 
        # number of occurrences
        primes = primes | Counter(prime_factors(i))
    smallest_mult = 1
    for item in primes.items():
        smallest_mult *= item[0]**item[1]
    return smallest_mult


# Yields the next prime number
# But is way too slow if calculating a large number of primes
def generate_primes():
    primes = [2]
    while True:
        current_prime = primes[-1]
        yield current_prime
        num = current_prime
        number_primes = len(primes)
        while current_prime == primes[-1]:
            num += 1
            j = 0
            while j < number_primes:
                if num % primes[j] == 0:
                    break
                j += 1
            if j == number_primes:
                primes.append(num)

# Returns an array of all primes 2<= p <n
def sieve_of_erastothenes(n):
    sieve = np.ones(n//3 + (n%6==2), dtype=bool)
    for i in range(1, int(((n**0.5)//3) + 1)):
        if sieve[i]:
            k=(3*i + 1)|1
            sieve[k*k//3::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return np.r_[2, 3, ((3*np.nonzero(sieve)[0][1:]+1)|1)]

# number_list: a list of integers that represent a long number
# n: # of digits to take the product of
# returns: max, digits
#   where max: max product of all n-digit combinations
#         digits: the digits that generate the max 
def largest_product_in_series(number_list, n):
    number_digits = len(number_list)

    products = [number_list[i:i+n] for i in range(number_digits-n)]
    max = 0
    digits = []
    for i in products:
        prod = np.prod(i)
        if prod > max:
            max, digits = prod, i
    return max, digits

def rel_a_to_b(a, s):
    return (s**2 - 2*a*s)/(2*s - 2*a)

"""A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

    a^2 + b^2 = c^2
    For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc."""
def pythagorean_triplet(s):
    """Rearranging the two equations, I get:
        b = (s/2 - a)/(1 + a/s)
    
    We also know for triangles that the sum of two sides must always 
    be longer than the third, so that we can go from 1 to s/2
    """
    for a in range(1, math.ceil(s/2)):
        b = rel_a_to_b(a, s)
        if (b).is_integer():
            c = math.sqrt(a**2 + b**2)

            if c.is_integer():
                d = a + b + c
                if d == s:
                    return a*b*c, a, b, c

    return None


def check_palindrome(pal):
    pal_string = str(pal)
    pal_length = len(pal_string)
    for i in range(math.floor(pal_length/2)):
        if pal_string[i] != pal_string[pal_length-1-i]:
            return False
    return True

# d: number of digits
def palindrome_product(d):
    init = int("9" * d)
    pals = []
    for i in range(init, 0, -1):
        for j in range(init, 0, -1):
            pal = i * j
            if check_palindrome(pal):
                pals.append(pal)
    return max(pals)

def sum_primes_below(n):
    primes = sieve_of_erastothenes(n)
    return sum(primes)

"""
Grid: 20x20 matrix
Returns: greatest product of four adjacent numbers (up, down, left, right, or diagonal)
"""
def grid_product(grid):
    """
    Algorithm:
        Sufficient to check: right, down, and diagonal
    """
    max_prod = 0
    grid_length = len(grid)
    for i in range(grid_length):
        row_length = len(grid[i])
        for j in range(row_length):
            the_point = grid[i][j]

            # To the right
            right_prod = 0
            if j < row_length - 4:
                right_prod = np.prod(grid[i][j:j+4])
            
            # Down
            down_prod = 0
            if i < grid_length - 4:
                down_prod = the_point
                for k in range(1, 4):
                    down_prod *= grid[i+k][j]

            # Diagonal
            diagonal_right_prod = 0
            if j < row_length - 4 and i < grid_length - 4:
                diagonal_right_prod = the_point
                for k in range(1, 4):
                    diagonal_right_prod *= grid[i+k][j+k]

            diagonal_left_prod = 0
            if j - 3 >= 0 and i < grid_length - 4:
                diagonal_left_prod = the_point
                for k in range(1, 4):
                    diagonal_left_prod *= grid[i+k][j-k]
            prods = [right_prod, diagonal_right_prod, diagonal_left_prod, down_prod]

            max_of_four = max(prods)
            if max_of_four > max_prod:
                max_prod = max_of_four
    return max_prod



"""
Nums is a list of length-n numbers, which are written as lists:
[[1, 3, 7, 4, ...], ... ]

Returns: The first ten digits of the sum of these numbers

TODO: This could be improved by summing progressively more digits 
        until the value of the first ten digits converges
"""
def first_ten_large_nums(nums, digits):
    sum = 0
    for j in range(digits):
        sum *= 10
        for i in range(len(nums)):
            sum += nums[i][j]
 
    return sum

"""
This can be optimized further to 
skip certain numbers that will surely yield short sequences
"""
def find_longest_collatz_under(n):
    lengths = {1: 1}
    for i in range(2, n):
        if i not in lengths:
            # All numbers 2^k will terminate quickly (i.e.: 8 -> 4 -> 2 -> 1 )
            log = math.log(i, 2)
            if (log).is_integer():
                lengths[i] = int(log) + 1
            else:
                c = collatz_sequence(i)
                c_list = []
                for j in c:
                    # Do not repeat calculations
                    # Eventually you will reach 1 and this operation will be performed
                    # This is the crucial step that speeds up the calculation
                    # This sped up my code by a factor of 10
                    if j in lengths:
                        j_length = lengths[j]
                        current_c_list_length = len(c_list)
                        for k in range(current_c_list_length):
                            # The length of the sequence starting at c_list[k]
                            # will be the length of the sequence starting at j, plus 
                            # the number of sequence elements already generated (current_c_list_length)
                            # minus the index of the current element (k)
                            lengths[c_list[k]] = j_length + current_c_list_length - k
                        break
                    c_list.append(j)
    max_length = max(lengths.items(), key=operator.itemgetter(1))
    return max_length


"""
Yields: next item in the Collatz sequence starting from n 
"""
def collatz_sequence(n):
    yield n
    while n != 1:
        if n%2 == 0:
            n = n//2
        else:
            n = 3*n + 1
        yield n

def construct_grid(s):
    grid = []
    for i in range(s + 1):
        grid.append([j for j in range(s + 1)])
    return grid

def create_adjacency_matrix(grid):
    grid_length = len(grid)

    matrix = [[0 for x in range(grid_length**2)] for y in range(grid_length**2)]
    for i in range(grid_length):
        row = grid[i]
        k = i * grid_length
        for j in range(len(row)):
            l = k+j
            # The node is k + j
            if j < len(row)-1:
                matrix[l][l+1] = 1
            if i < grid_length-1:
                matrix[l][l+grid_length] = 1
    return matrix

def dfs(matrix, start, path):
    # Can only go right and down
    paths = []
    m_length = len(matrix)
    for i in range(m_length):
        if matrix[start][i]:
            paths_1 = dfs(matrix, i, [*path, i])
            for p in paths_1:
                paths.append(p)
    if start == m_length - 1:
        return [path]
    return paths

"""
a and b are lists that begin with 1
"""
def greater_than(a, b):
    if len(a) > len(b):
        return True
    if len(a) < len(b):
        return False
    if a == b:
        return False
    for i in range(len(a)):
        if a[i] < b[i]:
            return False
    return True

def my_bit_add(a, b, c):
    if a and b and c:
        return [1, 1]
    if (a and b) or (a and c):
        return [1, 0]
    if a or b or c:
        return [0, 1]
    return [0, 0]

def my_add(a, b):
    
    len_a = len(a)
    len_b = len(b)
    if len_a < len_b:
        return my_add(b, a)
    carry = [0 for i in range(len_a + 1)]
    result = []
    len_difference = len_a - len_b
    for i in range(len_a):
        new_b = [*[0 for k in range(len_difference)], *b]
        bit_add = my_bit_add(a[len_a - 1 - i], new_b[len_a - 1 - i], carry[i])
        result.append(bit_add[1])
        carry[i+1] = bit_add[0]
    result.append(carry[len_a])

    correct_order = list(reversed(result))
    return correct_order[correct_order.index(1):]


def my_not(a):
    return [not i for i in a]

def my_negative(a):
    return [-1*a[0], *[a[1:]]]

"""
a and b are lists that begin with 1

Uses a - b = a + not(b) + 1
"""
def subtract(a, b):
    len_a = len(a)
    len_b = len(b)
    if len_a < len_b:
        return my_negative(subtract(b, a))
    
    

    return my_add(my_add(a, [1]), my_not(b))
"""
Both number and divisor are lists
"""
def long_division(dividend, divisor):
    quotient = [0]

    if divisor == [0]:
        raise ValueError('Cannot divide by zero')
    if greater_than(divisor, dividend):
        return quotient, dividend
    if divisor == dividend:
        return 1, 0
    remainder = dividend
    while greater_than(remainder, divisor) or remainder == divisor:
        remainder = subtract(remainder, divisor)
        quotient = my_add(quotient, [1])
    return remainder, quotient


def find_path_number(grid_size):
    return math.factorial(2*(grid_size))//math.factorial(grid_size)**2