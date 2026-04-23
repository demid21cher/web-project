import threading
import time


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_primes_in_range(start, end):
    primes = []
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)
    return primes


def find_primes_single_thread(start, end):
    primes = find_primes_in_range(start, end)
    return primes


def find_primes_multi_thread(start, end):
    mid = (start + end) // 2

    result1 = []
    result2 = []

    def worker(start, end, result_container):
        primes = find_primes_in_range(start, end)
        result_container.extend(primes)

    thread_1 = threading.Thread(target=worker, args=(start, mid, result1))
    thread_2 = threading.Thread(target=worker, args=(mid, end, result2))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    return sorted(result1 + result2)


if __name__ == "__main__":
    start = 1
    end = 1000000
    print("-" * 50)
    time_single_start = time.time()
    find_primes_single_thread(start, end)
    time_single_end = time.time()
    print(
        f"Time taken for single thread: {time_single_end - time_single_start} seconds"
    )
    print("-" * 50)
    time_multi_start = time.time()
    find_primes_multi_thread(start, end)
    time_multi_end = time.time()
    print(
        f"Time taken for multi-threading: {time_multi_end - time_multi_start} seconds"
    )
    print("-" * 50)

# Багатопотокова реалізація не забезпечує приросту продуктивності
# порівняно з однопотоковою для задач обчислювального характеру.
# Це пояснюється наявністю Global Interpreter Lock (GIL) у Python,
# який обмежує виконання байткоду одним потоком одночасно.
