import subprocess
import time


SCRIPTS = [
    "using_python.py",
    "using_pandas.py",
    "using_dask.py",
    "using_polars.py",
    "using_duckdb.py",
    "using_spark.py",
]


def run_benchmark():

    results = {}

    for script in SCRIPTS:
        print(f"\nExecutando {script}...")

        start = time.time()

        result = subprocess.run(
            ["poetry", "run", "python", f"src/{script}"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("ERRO:")
            print(result.stderr)

        end = time.time()

        if result.returncode != 0:
            print(f"{script} apresentou erro")

        results[script] = end - start

    return results


if __name__ == "__main__":

    benchmark_results = run_benchmark()

    print("\n========== RESULTADOS ==========")

    for script, seconds in sorted(
        benchmark_results.items(),
        key=lambda x: x[1]
    ):
        print(f"{script}: {seconds:.2f}s")