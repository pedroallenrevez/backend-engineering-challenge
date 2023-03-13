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
- Showcase systems-engineering by implementing the problem as a micro-service, with a message queue, and saving the metric somewhere.
- Showcase personal development with Nix.

### Non-Goals

- Losing too much time with Nix, integrating other services.

### Extra Personal Goals

1. Use Nix to build the python package;
2. " " declare CI/CD.
3. Learn websockets (w/ FastAPI)

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

Generate benchmark files:
```
poetry run unbabel generate_benchmark
```

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

======================================================
Algorithm complexity analysis: `O(n)`
======================================================

### Solution 3 - Optimizations using `numpy`

Solution 2 implements a simple algorithmic approach in pure python.
This can be sped up, since `numpy` uses `cython` hooks to improve computation times.
This means that the values themselves are translated into `C` objects.
Thus, our buffer stack arrays and calculations involving them can be improved by using these base-constructs.

### Solution 4 - Same bin optimizations

In the case of receiving samples that are incuded on the same bin, the algorithm would perform a lot of wasteful computations,
that would have to be upserted to the database.
Because we make productions until the leftmost timestamp of the current observation, if they are in the same 1-min bin, there would
be a lot of wasteful productions for this bin, that would have to be updated (upserted in this case).

So instead of running our algorithm at every sample, we would fill a 1-min buffer bin with these samples.

### Solution 5 - Do not do it in Python...

By simply implementing the algorithm in a language like `Go` or `Rust`,
computation times can be greatly increased, since `Python` is an interpreted language,
whereas `Go` and `Rust` are compiled and optimized.

### Benchmarking Algorithms

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

## Roadmap

Base Code

- [x] This Design Document quick-start (1H);
- [x] Do a Nix dev environment, with all needed dependencies (30m);
- [x] Prepare base backend-code of the two algorithms (4h);
- [x] Create benchmark test-bed for calcuation code(1h);
  - [x] Generation of test_size data
  - [x] Time execution
  - [x] Do benchmark for each
- [-] Structure code with pydantic models (15m).
  - [x] Models
  - [-] Implement code using models
- [x] Implement the CLI for the command (15m).
- [x] Have a CLI test script that processes a file with the 3 algorithms (5m).
- [x] Test Sliding window
  - [x] Base case
  - [x] Case with lots of timestamps within the same bin
  - [x] Case next observation is not within the time-window
  - [x] test against pandas
- [x] Write about the algorithm
- [x] Quality pass
  - [x] Typing, documentation
  - [x] refactor sliding window code and test code
  - [x] refactor sliding window consume function. otherwise the streaming function will not work
  - [-] pydantic code???
  - [x] conftest
- [x] fix tests

Service

- [x] Build server with psql, FastAPI, and webscokets
  - [x] create database code
  - [x] ingest a point to the database
  - [-] query code
  - [x] psql connector
  - [x] upserts
  - [-] FastAPI with CRUD
  - [x] FastAPI with websockets extension
  - [x] create websocket request on pkg
  - [x] separate code from pkg and server
  - [x] sliding window code packaged in server dockerfile
  - [x] API docker image
- [-] refactor out first and last



CI & Packaging

- [ ] Review code quality and documentation.
  - [x] ensure poetry entrypoints for script
  - [x] code is copied to serverside
  - [ ] do some logs server-side
  - [ ] still not packaged
  - [ ] recheck all code functionality
- [ ] Build introduction section on building and testing the code (15m).
- [ ] Iterate document and solutions, detailed explanation. Algo section rewrite
- [ ] Python poetry package (extra: with Nix).
- [ ] CI/CD with Github action (extra: with Nix).
- [x] Implement docker-compose running the app
- [x] Figure out how to use lefthook to commit to git, fork repo, and commit (30m).
- [-] Install scripts for nix environment (10m).

Extra

- [ ] React chakra front-end

## Conclusions

## Notes, TODOS, & questions

- How to keep poetry and nix dependencies separate, and how to keep the dev environment separated from poetry (think integration with `treefmt`).
