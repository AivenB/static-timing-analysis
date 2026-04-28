from enum import Enum


class PathType(Enum):
    MIN = "min"
    MAX = "max"


class SlackStatus(Enum):
    MET = "MET"
    VIOLATED = "VIOLATED"


class TimingPath:
    """A single timing path extracted from an STA report."""

    def __init__(
        self,
        startpoint: str,
        endpoint: str,
        path_group: str,
        path_type: PathType,
        arrival_time: float,
        required_time: float,
        slack: float,
        status: SlackStatus,
    ) -> None:
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.path_group = path_group
        self.path_type = path_type
        self.arrival_time = arrival_time
        self.required_time = required_time
        self.slack = slack
        self.status = status
