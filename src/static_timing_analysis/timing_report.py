from collections.abc import Iterable
from pathlib import Path

from static_timing_analysis.timing_path import PathType, SlackStatus, TimingPath


class TimingReport:

    def __init__(self, paths: list[TimingPath]) -> None:
        self.paths = paths

    @classmethod
    def from_file(cls, path: str | Path) -> "TimingReport":
        with open(Path(path), encoding="utf-8", errors="replace") as fh:
            return cls._parse_lines(fh)

    @classmethod
    def from_string(cls, text: str) -> "TimingReport":
        return cls._parse_lines(text.replace("\r\n", "\n").splitlines())

    @classmethod
    def _parse_lines(cls, lines: Iterable[str]) -> "TimingReport":
        paths: list[TimingPath] = []

        startpoint: str | None = None
        endpoint: str | None = None
        path_group: str | None = None
        path_type: str | None = None
        arrival_time: float | None = None
        required_time: float | None = None

        for raw_line in lines:
            line = raw_line.strip()

            if line.startswith("Startpoint:"):
                startpoint = line.split()[1]
                endpoint = None
                path_group = path_type = None
                arrival_time = required_time = None
                continue

            if startpoint is None:
                continue

            if line.startswith("Endpoint:"):
                endpoint = line.split()[1]
                continue

            if line.startswith("Path Group:"):
                path_group = line.split("Path Group:")[1].strip()
                continue

            if line.startswith("Path Type:"):
                path_type = line.split("Path Type:")[1].strip()
                continue

            tokens = line.split()

            if len(tokens) == 4 and tokens[1] == "data" and tokens[2] == "required":
                required_time = float(tokens[0])
                continue

            if len(tokens) == 4 and tokens[1] == "data" and tokens[2] == "arrival":
                arrival_time = abs(float(tokens[0]))
                continue

            if (
                len(tokens) == 3
                and tokens[1] == "slack"
                and startpoint is not None
                and endpoint is not None
                and path_group is not None
                and path_type is not None
                and arrival_time is not None
                and required_time is not None
            ):
                slack = float(tokens[0])
                status = SlackStatus(tokens[2].strip("()"))
                paths.append(TimingPath(
                    startpoint=startpoint,
                    endpoint=endpoint,
                    path_group=path_group,
                    path_type=PathType(path_type),
                    arrival_time=arrival_time,
                    required_time=required_time,
                    slack=slack,
                    status=status,
                ))
                startpoint = endpoint = None
                path_group = path_type = None
                arrival_time = required_time = None

        return cls(paths)

    def filter(
        self,
        status: SlackStatus | None = None,
        path_type: PathType | None = None,
        group: str | None = None,
    ) -> list[TimingPath]:
        result = self.paths
        if status is not None:
            result = [p for p in result if p.status == status]
        if path_type is not None:
            result = [p for p in result if p.path_type == path_type]
        if group is not None:
            result = [p for p in result if p.path_group == group]
        return result
