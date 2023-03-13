# Unbabel Challenge 2023

## Overview

The purpose of this challenge is to implement a system that is able to calculate a moving-average
in translation event data. Each translation event is a JSON object.

The objective of the challenge is to develop a CLI application that will read a text file with
multiple translation events, and calculate statistics for the provided file.

I will further develop on this proposal, by implementing a service, that emualtes a running-production system
that will stream these events, to be calculated and consumed by a database.

### Goals

- Build a python package with a CLI that allows calculating sliding window moving averages of translation events durations.
- Have proper dev environment, testing, benchmarking, and good code-conduct.
- Showcase planning, and means of communication.
- Showcase systems-engineering by implementing the problem as a micro-service, with websockets, and saving the metric somewhere.
- Showcase personal development with Nix.

### Non-Goals

- Losing too much time with Nix, integrating other services.

### Extra Personal Goals

1. Learn websockets (w/ FastAPI)

## Usage Guide

The following code is pakcaged with `poetry`, a kind of virtual environments for python.
Install poetry, and the package with:
```
pip install poetry
poetry install
```

Run tests:
```
poetry run pytest
```

Generate benchmark files and run benchmark:
```
poetry run unbabel generate_benchmark
poetry run unbabel benchmark
```

Run the application for a given input file, with our algorithm:
```
poetry run unbabel calculate input.txt output.txt --window-size 10 --strategy algo
```
(`strategy` alternatives [pandas|algo])

Start the database and API service:
```
docker-compose up
```
(Depending on the version you use, the command might be `docker-compose up`)

Test the ingestion service:
```
poetry run unbabel ingest
```

## Stack

The whole stack if comprised of three components:

- `postgres` docker image;
- API docker image;
- interaction CLI;

- service

  - `postgres` as a database to store the metrics
  - `docker` and `docker-compose` to package the application

- `python`

  - `typer` for CLI, and command line niceties
  - `fastapi` and `websockets` for the API
  - `pandas` for baseline solutions on rolling-window averages
  - `pydantic` for data-model validation, and databse ORM modelling

- development environment
  - `black`, `isort` and `treefmt` (included in the Nix devshell environment presets)
  - `pytest` for testing
  - `poetry` for building the package

## Detailed Design and Implementation details.

In this challenge I'm implementing two approaches, and benchmarking them to showcase results.

The first approach is simply a baseline, already made in `pandas`.

The second approach is an algorithmic approach, that intends to be incremental, meaning that it can be used in a service that is being streamed events, or batches of events.


### Solution 1 - Greedy approach with pandas

The first approach simply uses pandas resample function from `.csv` data, ingested from the json file.
A resampling is applied to the data, to make 1min bins, as per the provided example.
Then a simple rolling average over the window size is applied.

This will serve simply as a baseline to compare with our algorithmic approach.

### Solution 2 - Algorithmic approach

The baseline, that needs the whole input to be in memory (in case of a file), or
be calculated in chunks, obviously introduces a great overhead. `pandas` has no
way (that I know of) of dynamically calculating rolling statistics, by holding previous
observations in memory/state.

Thus, this algorithmic implementation, will receive irregularly sampled observations (1 or more),
and start producing rolling statistics. The algorithm is made in the way that it maintains state
for the duration of the rolling-window size. So, if the window size is 10 minutes, then it will hold
all observations within those 10 minutes.

This algorithm makes use of two buffers that maintain state, and keep the needed information to a minimum.

1. `stack` - the stack holds the observation values themselves, in order to calculate the statistic (in this case, an average);
2. `diffs` - the time-difference buffer holds the difference in time (timedelta) between seen observations. With this, we can avoid
   storing useless timestamp data, for multiple points.

This algorithm uses the following terminology:

- `leftmost timestamp` - given a timestamp, it's leftmost value will be the "floor" of the timestamp. i.e. `leftmostts(00:00:03:234234)=00:00:03`
- `rightmost timestamp` - " ", the rightmost value will be the "ceiling" of the timestamp. i.e. `rightmostts(00:00:03:234234)=00:00:04`
- `first` is the first observed value within bounds of the rolling-window;
- `last` is the last observed value within bounds of the rolling-window;

The sliding window algorithm, consumes 1 sample at a time:

1. An observation is read from a stream/file;
2. The stack is filled with the observation value, and the timedelta calculated from the timestamp (relative to previous observation);
3. Forward fill 1 min timestamps are generated until the leftmost timestamp of the current observed timestamp, and statistic calculated from the current state of the stack;
4. Rinse and repeat.

A couple notes on the algorithm:

- First and last observations are special cases.
  - The first observation, that initiates the algorithm will always be 0-valued.
  - Given that the algorithm produces the statistics all the way until the next-observation, it means that the last statistic will not be calculated within normal iterations of the algorithm. This means that we "manually" flush the buffer at the end of the iteration, if we want to finish the algorithm and not feed it more data.
- On step 3, when we are forward filling timestamps, the time-difference stack is observed to see if the generated timestamp is still within the bounds of the rolling-window.

The code is commented throughout, adding to this explanation.

This simplistic approach has a couple of downsides though:

1. Can be optimized to look for next observations within the same bin, avoiding unnecessary productions and works.
2. If the observations are too granular, and the window size too big, some memory problems might occur.


## Further Optimizations
### Using with Numpy

Solution 2 implements a simple algorithmic approach in pure python.
This can be sped up, since `numpy` uses `cython` hooks to improve computation times.
This means that the values themselves are translated into `C` objects.
Thus, our buffer stack arrays and calculations involving them can be improved by using these base-constructs.

### Same bin optimizations

In the case of receiving samples that are incuded on the same bin, the algorithm would perform a lot of wasteful computations,
that would have to be upserted to the database.
Because we make productions until the leftmost timestamp of the current observation, if they are in the same 1-min bin, there would
be a lot of wasteful productions for this bin, that would have to be updated (upserted in this case).

So instead of running our algorithm at every sample, we would fill a 1-min buffer bin with these samples.

### Do not do it in Python...

By simply implementing the algorithm in a language like `Go` or `Rust`,
computation times can be greatly increased, since `Python` is an interpreted language,
whereas `Go` and `Rust` are compiled and optimized.

## Benchmarking Algorithms

Read the introduction section on how to run the benchmark and generate input files for it.

| (in seconds)    | Pandas | Algo   |
| --------------- | ------ | ------ |
| Challenge Input | 0.007  | 0.0004 |
| 1K              | 0.6    | 0.14   |
| 10K             | 6      | 1.4    |
| 100K            | 83     | 14     |
| 1M              | 749    | 171    |

## Postgres DB Ingestion Service

Considerations & Optimizations:

- We are upserting each row individually, of course, if done in bulk, DB interaction times will improve, and be faster;
- Simplified interaction with DB with `psycopg2`. More advanced and complex DB models, could use `sqlalchemy` to manage relations.


## Conclusions

