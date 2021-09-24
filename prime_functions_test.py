import unittest
from prime_functions import *

class LargestPrimeTestCase(unittest.TestCase):

    def test_prime_factors(self):
        # Test ValueError thrown
        with self.assertRaises(ValueError):
            prime_factors(-5)
        
        # Test obvious simple cases
        self.assertEqual(prime_factors(0), [])
        self.assertEqual(prime_factors(1), [])
        self.assertEqual([2], prime_factors(2))
    
    def test_prime_factors_2(self):
        self.assertEqual([3], prime_factors(3))
        self.assertEqual([5], prime_factors(5))
        self.assertEqual([3, 3], prime_factors(9))
        self.assertEqual(prime_factors(4), [2, 2])
        self.assertEqual(prime_factors(10), [2, 5])
        
        # Test project Euler case
        self.assertEqual(set(prime_factors(13195)), {5, 7, 13, 29})

        self.assertEqual(max(prime_factors(600851475143)), 6857)

    @unittest.expectedFailure
    def test_prime_factors_3(self):
        prime_factors(2, primes=[])
        self.assertEqual([2, 3], prime_factors(3))

    def test_all_divisors(self):
        self.assertEqual(all_divisors(-4), set([-1, 2, 4]))
        self.assertEqual(all_divisors(0), set([]))
        self.assertEqual(all_divisors(1), set([1]))
        self.assertEqual(all_divisors(3), set([1, 3]))
        self.assertEqual(all_divisors(6), set([1, 2, 3, 6]))
        self.assertEqual(all_divisors(28), set([1,2,4,7,14,28]))

    def test_natural_numbers(self):
        n = natural_number_generator()
        ns = [next(n) for i in range(5)]
        self.assertEqual(ns, [1, 2, 3, 4, 5])

    def test_triangle_numbers(self):
        triangle_number = triangle_number_generator()
        triangles = [next(triangle_number) for i in range(5)]
        self.assertEqual(triangles, [1, 3, 6, 10, 15])

    def test_triangle_divisors(self):
        self.assertEqual(triangle_divisors(5), 28)
    
    @unittest.skip('Takes too long')
    def test_triangle_divisors_500(self):
        self.assertEqual(triangle_divisors(500), 76576500)

    def test_smallest_multiple(self):
        self.assertEqual(1, smallest_multiple(1))
        self.assertEqual(2, smallest_multiple(2))
        self.assertEqual(6, smallest_multiple(3))
        self.assertEqual(12, smallest_multiple(4))
        self.assertEqual(2520, smallest_multiple(10))
        self.assertEqual(232792560, smallest_multiple(20))
    
    def test_negative_number(self):
        with self.assertRaises(ValueError):
            smallest_multiple(-1)

    def test_generate_first_six_primes(self):
        gen = generate_primes()
        first_six = [next(gen) for i in range(6)]
        expected_first_six = [2, 3, 5, 7, 11, 13]
        self.assertEqual(expected_first_six, first_six)

    @unittest.skip('Takes too long')
    def test_generate_10001_prime(self):
        new_gen = generate_primes()
        for i in range(10000):
            next(new_gen)

        self.assertEqual(104743, next(new_gen))

    def test_sum_of_primes(self):
        self.assertEqual(sum_primes_below(10), 17)
        self.assertEqual(sum_primes_below(2*10**6), 142913828922)

    def test_largest_product(self):
        number_list = []
        with open('thousand_digit_number.txt') as large_number_reader:
            for line in large_number_reader:
                number_list = [*number_list, *list(map(int, line.strip()))]

        self.assertEqual((5832, [9, 9, 8, 9]), largest_product_in_series(number_list, 4))
        self.assertEqual((23514624000, [5, 5, 7, 6, 6, 8, 9, 6, 6, 4, 8, 9, 5]), largest_product_in_series(number_list, 13))

    def test_pythagorean_triplet(self):
        self.assertEqual(pythagorean_triplet(12), (3*4*5, 3, 4, 5))

        self.assertEqual(pythagorean_triplet(1000), (31875000, 200, 375, 425))

    def test_palindrome_product(self):
        self.assertEqual(palindrome_product(2), 9009)
        self.assertEqual(palindrome_product(3), 906609)

    def test_grid_product(self):
        grid = []
        with open('grid_numbers.txt') as grid_numbers:
            for line in grid_numbers:
                grid.append(list(map(int, line.strip().split(' '))))

        self.assertEqual(grid_product(grid), 70600674)

    def test_fifty_digit(self):
        numbers = []
        with open('50_digit_nums.txt') as nums:
            for line in nums:
                numbers.append(list(map(int, line.strip())))
        self.assertEqual(first_ten_large_nums(numbers, 11), 5537376230342)
        # print('\n', first_ten_large_nums(numbers, 13))
        # print(first_ten_large_nums(numbers, 10))
        # print(first_ten_large_nums(numbers, 8))
        # print(first_ten_large_nums(numbers, 15))
        # print(first_ten_large_nums(numbers, 12))

    def test_collatz_sequence(self):
        c1 = collatz_sequence(1)
        self.assertEqual([1], [i for i in c1])

        c2 = collatz_sequence(13)
        self.assertEqual([13, 40, 20, 10, 5, 16, 8, 4, 2, 1], [i for i in c2])

    def test_find_longest_collatz(self):
        self.assertEqual(find_longest_collatz_under(10), (9, 20))

    def test_find_longest_collatz2(self):
        self.assertEqual(find_longest_collatz_under(10**6), (837799, 525))

    @unittest.skip('Takes about 13 seconds to run')
    def test_find_longest_collatz3(self):
        self.assertEqual(find_longest_collatz_under(10**7), (8400511, 686))

    def test_find_all_paths(self):
        self.assertEqual([[0, 1, 2], [0, 1, 2], [0, 1, 2]], construct_grid(2))
        grid = construct_grid(2)
        expected_matrix = [ [0, 1, 0, 1, 0, 0, 0, 0, 0], 
                            [0, 0, 1, 0, 1, 0, 0, 0, 0], 
                            [0, 0, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]
                            ] 
        matrix = create_adjacency_matrix(grid)
        self.assertEqual(expected_matrix, matrix)
        self.assertEqual(6, find_path_number(2))
        self.assertEqual(20, find_path_number(3))

        self.assertEqual(137846528820, find_path_number(20))

    def test_my_add(self):
        self.assertEqual(my_add([1, 0, 0, 1], [1, 0]), [1, 0, 1, 1])
        self.assertEqual(subtract([1, 0, 1, 0], [1, 1]), [1, 1, 1])

