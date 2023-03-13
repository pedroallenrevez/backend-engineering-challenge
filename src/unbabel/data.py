import random
from enum import Enum

import pandas as pd
from pydantic import BaseModel, NonNegativeFloat, PositiveInt

# from uuid import UUID


class Languages(str, Enum):
    EN = "en"
    PT = "pt"
    FR = "fr"


class Client(str, Enum):
    AIRLIBERTY = "airliberty"
    # etc


class Event(str, Enum):
    DELIVERED = "translation_delivered"
    ON_TRANSIT = "translation_doing"
    # etc


class TranslationEvent(BaseModel):
    """Data-model for a translation event message.

    Args:
        BaseModel (_type_): _description_

    TODO:
        - [x] Positive duration, nr words
        - [x] UUID
        - [ ] Optional pandas
    """

    timestamp: pd.Timestamp  # 2018-12-26 18:12:19.903159,
    # timestamp: datetime #2018-12-26 18:12:19.903159,
    translation_id: str  # 5aa5b2f39f7254a75aa4,
    source_language: Languages  # en,
    target_language: Languages  # fr,
    client_name: Client  # airliberty,
    event_name: Event  # translation_delivered,

    duration: PositiveInt  # In minutes #20,
    nr_words: PositiveInt

    @classmethod
    def generate(cls, size: int = 100):
        init_ts = pd.Timestamp("2018-12-26 18:11:08.509654")
        ts = init_ts
        for _ in range(size):
            # minute = random.randint(0, 5)
            seconds = random.randint(100, 999)
            random_delta = pd.Timedelta(f"P0DT0H0M{seconds}.456S")
            ts += random_delta
            yield cls(
                timestamp=ts,
                translation_id="5aa5b2f39f7254a75bb3",
                source_language=Languages.EN,
                target_language=Languages.PT,
                client_name=Client.AIRLIBERTY,
                event_name=Event.DELIVERED,
                duration=random.randint(1, 100),
                nr_words=20,
            )


class MovingAverage(BaseModel):
    date: pd.Timestamp
    average_delivery_time: NonNegativeFloat
