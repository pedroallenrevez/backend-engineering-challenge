import datetime
import json
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import pandas as pd

JSONString = str
TimeData = Tuple[(datetime.datetime | pd.Timestamp), (float | int)]
JsonValidTimeData = Tuple[str, (float | int)]


def txt_to_csv(txt: str) -> pd.DataFrame:
    """Helper function to turn a txt file with a Json object at each line,
    to a pandas Dataframe.

    Args:
        txt (str): The read file contents

    Returns:
        pd.DataFrame: A dataframe indexed on timestamp, with the duration of the events.
    """
    data = []
    for l in txt.split("\n"):
        if l.strip():
            datum = json.loads(l)
            data.append((pd.Timestamp(datum["timestamp"]), datum["duration"]))
    return pd.DataFrame(data=data, columns=["timestamp", "duration"]).set_index(
        "timestamp"
    )


def leftmostts(ts: datetime.datetime) -> datetime.datetime:
    """Calculates the leftmost value of a timestamp.

    i.e. leftmostts(00:00:12.123123) = 00:00:12

    Args:
        ts (datetime.datetime): A timestamp

    Returns:
        datetime.datetime: The floor of the timestamp.
    """
    return ts.replace(second=0, microsecond=0)


def rightmostts(ts: datetime.datetime) -> datetime.datetime:
    """Calculates the leftmost value of a timestamp.

    i.e. rightmostts(00:00:12.123123) = 00:00:13

    Args:
        ts (datetime.datetime): A timestamp

    Returns:
        datetime.datetime: The ceiling of the timestamp.
    """
    return leftmostts(ts) + datetime.timedelta(minutes=1)


def produce_json(
    date: (datetime.datetime | pd.Timestamp), duration: float
) -> JSONString:
    """Produce a Json string to be appended to a file

    Args:
        date (datetime.datetime  |  pd.Timestamp): The timestamp of the event.
        duration (float): The calculated moving average of the event.

    Returns:
        JSONString: JSON serialized string.
    """
    return json.dumps(produce_dict(str(date), duration))


def produce_dict(date: (datetime.datetime | pd.Timestamp), duration: float) -> dict:
    """Produce a dict with date and average_delivery_time keys.

    Args:
        date (datetime.datetime  |  pd.Timestamp): The timestamp of the event.
        duration (float): The calculated moving average of the event.

    Returns:
        dict: A dictionary with output values for rolling-window statistics
    """
    return {"date": str(date), "average_delivery_time": duration}


def produce_timedata(date: datetime.datetime, duration: float) -> JsonValidTimeData:
    """Produce a dict with date and average_delivery_time keys.

    Args:
        date (datetime.datetime  |  pd.Timestamp): The timestamp of the event.
        duration (float): The calculated moving average of the event.

    Returns:
        TimeData: A tuple with timestamp and duration.
    """
    return (str(date), duration)


def parse_json_line(line: JSONString) -> TimeData:
    """Parses a JsonString into a tuple of timestamp and duration, the only information we need
    to calculate a rolling-window.

    Args:
        line (JSONString): A string value that holds a json-valid object.

    Returns:
        TimeData: A tuple with timestamp and duration.
    """
    c = json.loads(line)
    return (datetime.datetime.fromisoformat((c["timestamp"])), c["duration"])


def moving_window_pandas(df: pd.DataFrame, window_size: int = 10) -> pd.DataFrame:
    """Calculate a moving average of a dataframe with given window size in minutes

    NOTE: According to the provided examples in the challenges README,
    1 minute bins are assumed.

    Args:
        df (pd.DataFrame): A Dataframe that holds the metrics to be rolled over.
        window_size (int, optional): The size of the rolling window in minutes. Defaults to 10.

    Returns:
        pd.DataFrame: A dataframe with rolling averages of provided metrics.
    """
    # We use `label=right` to denote that we want the resampling operation to be
    # resample the points to the left of the timestamp.
    return (
        df.resample("1T", label="right").mean().rolling(window=f"{window_size}T").mean()
    )


def strategy_pandas(input_file: Path, window_size: int) -> Iterable[JSONString]:
    """Greedy algorithmic approach, for baseline measurements.
    Uses in-memory pandas calculations to do a rolling average of a metric.

    Downsides:
    1. Needs to hold the whole file in-memory, so it is not suitable for big workloads.
    2. Is not an incremental algorithm, thus we need to hold all values in a DataFrame.

    Args:
        input_file (Path): The file to read Json lines from.
        window_size (int): The rolling window size in minutes.

    Yields:
        JSONString: A JSONString ready to be appended to a file.
    """
    df = txt_to_csv(open(input_file, "r").read())
    df = moving_window_pandas(df, window_size=window_size)
    for _, row in df.iterrows():
        yield produce_json(row.name, row["duration"])


class SlidingWindow:
    def __init__(self, window: int):
        """The Sliding window algorithm implementation.
        The class maintains state, and consumes inputs one by one, while producing
        1-min bins with the values.

        Args:
            window (int): The size of the rolling window in minutes.
        """
        self.stack: List[float] = []
        self.tss: List[datetime.datetime] = []

        self.first: Optional[datetime.datetime] = None
        self.last: Optional[datetime.datetime] = None

        self.window = window  # in minutes

    def mean(self, stack: List[float]) -> float:
        """Calculates the mean of the value-stack/rolling-window.

        Args:
            stack (List[float]): A buffer of values within the rolling-window.

        Returns:
            float: Mean value of the stack.
        """
        len_ = len(stack)
        if len_ == 0:
            return 0.0
        return float(sum(stack) / len(stack))

    def forward(self, value: TimeData):
        """Sliding window incremental step.
        Consumes a value from the array and populates:
        1. Timestamp stack (`self.tss`) with the timestamps of seen values;
        2. Value-stack (`self.stack`) with the actual duration value.

        Args:
            value (TimeData): The value we are consuming, composed of timestamp and duration.
        """
        ts, dur = value
        # if iterating for the first time, we set the first timestamp to the seen value
        if self.first is None:
            self.first = ts

        # Update the "previous observed value" (first) to be the value of last iteration (last)
        if self.first is not None and self.last is not None:
            self.first = self.last

        # current observation is the last observed value
        self.last = ts
        self.stack.append(dur)
        self.tss.append(ts)

    def pop(self):
        """Helper function to control the stack of values.

        When the window buffer is full, it means that the first value
        on the stack is out of range of the rolling-window.
        """
        # pop the first value from both stacks
        self.stack = self.stack[1:]
        ts = self.tss[0]
        self.tss = self.tss[1:]
        assert (
            self.first is not None
        ), "Shouldn't happen. Tried to pop stack without iterating values first."
        # Update the value of first timestamp in window to the next value in the stack
        self.first = ts
        assert self.first is not None and self.last is not None
        assert self.first <= self.last, (str(self.first), str(self.last))

    def consume(self, c: TimeData) -> List[JsonValidTimeData]:
        results: List[JsonValidTimeData] = []
        # c = parse_json_line(c)
        ts, _ = c
        # Update stacks with new observed value
        self.forward(c)

        lts = leftmostts(ts)
        # if it's the first observed value, the left-most timestamp (floor of timestamp)
        # will have no samples in it's bin, and thus the value is 0
        if self.first == self.last:
            # results.append(produce_json(lts, 0.0))
            results.append(produce_timedata(lts, 0.0))
        else:
            # ffill from last to lts
            assert self.first is not None and self.last is not None
            its = rightmostts(self.first)
            while its <= leftmostts(self.last):
                # calculate bin average (except for the current observation, last value added on
                # the stack)
                results.append(produce_timedata(its, self.mean(self.stack[:-1])))
                # we iterate in 1min bins
                its += datetime.timedelta(minutes=1)

                # if our first value on the stack is out of bounds then pop it
                if its - self.tss[0] > datetime.timedelta(minutes=10):
                    # if window is bust, then we have to pop values from our stacks
                    self.pop()
        return results

    def flush(self) -> List[JsonValidTimeData]:
        # This algorithm produces 1min bins until the leftmost timestamp of the
        # current observation.
        # This means that for the last observation, there will be no production
        # of values, because there are no observations left
        # So we do it manually by flushing our stack.
        assert self.last is not None
        return [produce_timedata(rightmostts(self.last), self.mean(self.stack))]


def strategy_sliding_window(input_file: Path, window_size: int) -> Iterable[JSONString]:
    """Main routine for incremental calculation of moving-averages using a sliding window.

    Args:
        input_file (Path): The file to read Json lines from.
        window_size (int): The rolling window size in minutes.

    Yields:
        JSONString: A JSONString ready to be appended to a file.
    """
    window = SlidingWindow(window_size)
    fp = open(input_file, "r")
    while (c := fp.readline()) != "":
        d = parse_json_line(c)
        for ts, dur in window.consume(d):
            yield produce_json(ts, dur)
    ts, dur = window.flush()[0]
    yield produce_json(ts, dur)
