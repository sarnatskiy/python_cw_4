import time
import statistics
import asyncio

import phil
import async_phil


def benchmark_sync(start, finish, n_runs=3):
    times = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        graph = phil.build_graph(start, finish)
        phil.find_chain(graph, start, finish)
        times.append(time.perf_counter() - t0)
    return times


async def benchmark_async(start, finish, n_runs=3):
    times = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        graph = await async_phil.build_graph(start, finish)
        async_phil.find_chain(graph, start, finish)
        times.append(time.perf_counter() - t0)
    return times


def report(title, times):
    print(f"{title}:")
    print(f"  runs   = {len(times)}")
    print(f"  mean   = {statistics.mean(times):.4f}s")
    print(f"  median = {statistics.median(times):.4f}s")
    print(f"  min    = {min(times):.4f}s")
    print(f"  max    = {max(times):.4f}s\n")


if __name__ == "__main__":
    start, finish = "Математика", "Философия"

    print(f"Benchmark: {start} -> {finish}\n")

    async_times = asyncio.run(benchmark_async(start, finish, n_runs=3))
    report("Async", async_times)

    sync_times = benchmark_sync(start, finish, n_runs=3)
    report("Sync", sync_times)

    speedup = statistics.mean(sync_times) / statistics.mean(async_times)
    print(f"Speedup (sync/async): {speedup:.2f}x")
