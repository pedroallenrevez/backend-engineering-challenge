from src.unbabel.calc import (
    SlidingWindow,
    moving_window_pandas,
    parse_json_line,
    produce_json,
    txt_to_csv,
)


def test_pandas(test_file, test_file_output):
    df = txt_to_csv(test_file)
    df = moving_window_pandas(df, window_size=10)
    output_tokens = test_file_output.split("\n")
    for i, (_, row) in enumerate(df.iterrows()):
        assert produce_json(row.name, row["duration"]) == output_tokens[i + 1]


def generic_window(test_file, test_file_output):
    window = SlidingWindow(10)
    output_tokens = test_file_output.split("\n")
    results = []
    for c in test_file.split("\n"):
        d = parse_json_line(c)
        for ts, dur in window.consume(d):
            results.append(produce_json(ts, dur))
    ts, dur = window.flush()[0]
    results.append(produce_json(ts, dur))
    for i, r in enumerate(results):
        assert r == output_tokens[i]


def test_window(test_file, test_file_output):
    generic_window(test_file, test_file_output)


def window_vs_pandas(test_file):
    # pandas
    df = txt_to_csv(test_file)
    df = moving_window_pandas(df, window_size=10)
    df = df.fillna(0)

    # window
    window = SlidingWindow(10)
    results = []
    for c in test_file.split("\n"):
        d = parse_json_line(c)
        for ts, dur in window.consume(d):
            results.append(produce_json(ts, dur))
    ts, dur = window.flush()[0]
    results.append(produce_json(ts, dur))

    for i, (_, row) in enumerate(df.iterrows()):
        pd_production = produce_json(row.name, row["duration"])
        assert pd_production == results[i + 1]


def test_window_vs_pandas_test_file(test_file):
    window_vs_pandas(test_file)


def test_window_vs_pandas_test_file2(test_file2):
    window_vs_pandas(test_file2)


def test_window_next_observation_out_of_range(test_file_out_of_range):
    window_vs_pandas(test_file_out_of_range)


def test_window_next_observation_out_of_range_last(test_file_out_of_range_last):
    window_vs_pandas(test_file_out_of_range_last)


def test_window_mult_within_same_bin(
    test_file_mult_within_bin, test_file_mult_within_bin_output
):
    """This test requires manual checking due to pandas resampling to 1min bins,
    makes the rolling-window calculations wrong.
    """
    generic_window(test_file_mult_within_bin, test_file_mult_within_bin_output)
