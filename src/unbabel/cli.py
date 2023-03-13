import asyncio
from enum import Enum
from pathlib import Path
from time import time
from typing import Dict, Tuple

import typer
import websockets

from .calc import strategy_pandas, strategy_sliding_window
from .data import TranslationEvent

app = typer.Typer()


class Strategy(str, Enum):
    PANDAS = "pandas"
    ALGO = "algo"
    SERVICE = "service"


STRATEGY_FN = {
    Strategy.PANDAS: strategy_pandas,
    Strategy.ALGO: strategy_sliding_window,
}


@app.command()
def generate(
    output_file: Path,
    test_size: int = 1000,
):
    """Generate a file with given size, of translation event data.

    Args:
        output_file (Path): _description_
        test_size (int, optional): _description_. Defaults to 1000.
    """
    print(f"Generating an input file with size {test_size}")

    with open(output_file, "w") as fp:
        for d in TranslationEvent.generate(size=test_size):
            fp.write(d.json() + "\n")


@app.command()
def generate_benchmark():
    for output_file, test_size in [
        ("dev/input_1K.txt", 1000),
        ("dev/input_10K.txt", 10000),
        ("dev/input_100K.txt", 100000),
        ("dev/input_1M.txt", 1000000),
    ]:
        output_path = Path(output_file)
        generate(output_path, test_size)


@app.command()
def calculate(
    # input_file: Optional[Path] = None,
    input_file: Path,
    output_file: Path,
    window_size: int = 10,
    strategy: Strategy = Strategy.PANDAS,
):
    """Calculate moving-averages over an input file.

    Use --strategy to select the method of calculating the statistic.\n
    Use --test-size to increase the default sample size of the input file.\n
    Alter --window-size to modify the moving-average in minutes.\n
    """
    start = time()
    strategy_fn = STRATEGY_FN[strategy]
    fhandle = open(output_file, "a")
    for d in strategy_fn(input_file, window_size=window_size):
        fhandle.write(d + "\n")
    print(f"Took {time() - start} seconds")


@app.command()
def benchmark():
    """Benchmark the algorithms versus the various file sizes."""
    results: Dict[Tuple[Strategy, str], float] = {}
    for strat in [Strategy.PANDAS, Strategy.ALGO]:
        for input_file in [
            "dev/input.txt",
            "dev/input_1K.txt",
            "dev/input_10K.txt",
            "dev/input_100K.txt",
            "dev/input_1M.txt",
        ]:
            print(strat, input_file)
            input_path = Path(input_file)
            start = time()
            strategy_fn = STRATEGY_FN[strat]
            for _ in strategy_fn(input_path, window_size=10):
                pass
            total_time = time() - start
            print(f"Took {total_time} seconds.")
            results[(strat, input_file)] = total_time
    print(results)


async def ingestws(
    test_size: int = 1000,
):
    """Generates random events, calculates statistics and ingests them to
    a Postgres database.

    For now keep the windowing code client-side to test the server.
    Then move the code to server-side, and modify needed optimizations.
    """
    # window = SlidingWindow(window_size)
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        for i, d in enumerate(TranslationEvent.generate(size=test_size)):
            print(f"{i} / {test_size}", end='\r')
            await websocket.send(d.json())
            _ = await websocket.recv()


@app.command()
def ingest(
    test_size: int = 1000,
):
    asyncio.get_event_loop().run_until_complete(ingestws(test_size))

def main():
    app()

if __name__ == "__main__":
    main()
