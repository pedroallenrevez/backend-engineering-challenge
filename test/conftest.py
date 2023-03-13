import pytest


@pytest.fixture
def test_file():
    return """{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}"""


@pytest.fixture
def test_file2():
    return """{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:18:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 10}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}"""


@pytest.fixture
def test_file_out_of_range_last():
    return """{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:43:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 60}"""


@pytest.fixture
def test_file_out_of_range():
    return """{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:43:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:45:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 60}"""


@pytest.fixture
def test_file_mult_within_bin():
    return """{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903160","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903161","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903162","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903163","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903164","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903165","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903166","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903167","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903168","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903169","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903170","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:19.903171","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:43:19.903173","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}"""


@pytest.fixture
def test_file_output():
    return """{"date": "2018-12-26 18:11:00", "average_delivery_time": 0.0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}"""


@pytest.fixture
def test_file_mult_within_bin_output():
    return """{"date": "2018-12-26 18:11:00", "average_delivery_time": 0.0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 52.23076923076923}
{"date": "2018-12-26 18:25:00", "average_delivery_time": 52.23076923076923}
{"date": "2018-12-26 18:26:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:27:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:28:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:29:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:30:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:31:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:32:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:33:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:34:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:35:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:36:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:37:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:38:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:39:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:40:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:41:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:42:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:43:00", "average_delivery_time": 54.0}
{"date": "2018-12-26 18:44:00", "average_delivery_time": 54.0}"""
