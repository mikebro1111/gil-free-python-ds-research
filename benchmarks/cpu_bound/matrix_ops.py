import numpy as np
import threading
import time
from src.utils.profiler import profile


@profile
def matrix_multiply(size=1024):
    """
    Generates and multiplies two random matrices.

    Args:
        size (int, optional): The size of the matrices. Defaults to 1024.

    Returns:
        np.ndarray: The result of the matrix multiplication.
    """
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return np.dot(A, B)


def run_matrix_experiment():
    """
    Runs a matrix multiplication experiment with varying matrix sizes and thread counts.

    Returns:
        dict: A dictionary containing the average execution times for each combination of matrix size and thread count.
    """
    sizes = [256, 512, 1024]
    threads = [1, 2, 4, 8]

    results = {}
    for size in sizes:
        for n_threads in threads:
            times = []
            for _ in range(3):  # 3 iterations for stability
                start = time.perf_counter()

                workers = []
                for _ in range(n_threads):
                    t = threading.Thread(target=matrix_multiply, args=(size,))
                    workers.append(t)
                    t.start()

                for t in workers:
                    t.join()

                elapsed = time.perf_counter() - start
                times.append(elapsed)

            results[(size, n_threads)] = np.mean(times)

    return results