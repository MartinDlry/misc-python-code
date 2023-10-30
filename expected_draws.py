import fractions
from functools import lru_cache
from collections import defaultdict

'''
Returns the expected number of draws to get n outcomes m times each in total, where all n options are equally likely
'''
def expected_draws_rec(n, m):
    n = fractions.Fraction(n)

    @lru_cache(maxsize=None)
    def rec(case):
        if case[-1] == n:
            return 0

        remaining = n - case[-1]
        expected_draws_for_new = n / remaining

        sum_of_next_cases = 0
        for i, (count, next_count) in enumerate(zip(case, case[1:])):
            if count != 0:
                next_case = case[:i] + (count-1, next_count + 1) + case[i+2:]
                probability = count / remaining
                sum_of_next_cases += probability * rec(next_case)
        
        return expected_draws_for_new + sum_of_next_cases
     
    return rec((int(n),) + (0,)*m)

def expected_draws(n, m):
    expected_draws_ = 0
    cases_probabilities = {(n,) + (0,)*m : fractions.Fraction(1)}
    for _ in range(n*m):
        next_layer_probabilities = defaultdict(lambda: 0)
        for case, probability in cases_probabilities.items():
            remaining = n - case[-1]
            expected_draws_ += probability * n / remaining
            for i, (count, next_count) in enumerate(zip(case, case[1:])):
                if count != 0:
                    next_case = case[:i] + (count-1, next_count + 1) + case[i+2:]
                    next_layer_probabilities[next_case] += probability * count / remaining

        cases_probabilities = next_layer_probabilities

    return expected_draws_

if __name__ == "__main__":
    n = 5
    m = 5

    result = float(expected_draws(n, m))
    result_rec = float(expected_draws_rec(n, m))

    assert result == result_rec

    print(f'Expected draws for {n} outcomes {m} times: {result}')