import pytest

from static_timing_analysis.timing_path import PathType, SlackStatus, TimingPath


class TestPathType:
    def test_min_value(self) -> None:
        assert PathType.MIN.value == "min"

    def test_max_value(self) -> None:
        assert PathType.MAX.value == "max"

    def test_from_string(self) -> None:
        assert PathType("min") == PathType.MIN
        assert PathType("max") == PathType.MAX

    def test_invalid_value(self) -> None:
        with pytest.raises(ValueError):
            PathType("invalid")


class TestSlackStatus:
    def test_met_value(self) -> None:
        assert SlackStatus.MET.value == "MET"

    def test_violated_value(self) -> None:
        assert SlackStatus.VIOLATED.value == "VIOLATED"

    def test_from_string(self) -> None:
        assert SlackStatus("MET") == SlackStatus.MET
        assert SlackStatus("VIOLATED") == SlackStatus.VIOLATED

    def test_invalid_value(self) -> None:
        with pytest.raises(ValueError):
            SlackStatus("invalid")


class TestTimingPath:
    def _make_path(
        self,
        slack: float = 5.0,
        status: SlackStatus = SlackStatus.MET,
        path_type: PathType = PathType.MAX,
    ) -> TimingPath:
        return TimingPath(
            startpoint="reg_a",
            endpoint="reg_b",
            path_group="clk",
            path_type=path_type,
            arrival_time=5.0,
            required_time=10.0,
            slack=slack,
            status=status,
        )

    def test_construction(self) -> None:
        path = self._make_path()
        assert path.startpoint == "reg_a"
        assert path.endpoint == "reg_b"
        assert path.path_group == "clk"
        assert path.path_type == PathType.MAX
        assert path.arrival_time == 5.0
        assert path.required_time == 10.0
        assert path.slack == 5.0
        assert path.status == SlackStatus.MET

    def test_zero_slack(self) -> None:
        path = self._make_path(slack=0.0, status=SlackStatus.MET)
        assert path.slack == 0.0

    def test_negative_slack(self) -> None:
        path = self._make_path(slack=-2.5, status=SlackStatus.VIOLATED)
        assert path.slack == -2.5
        assert path.status == SlackStatus.VIOLATED

    def test_min_path_type(self) -> None:
        path = self._make_path(path_type=PathType.MIN)
        assert path.path_type == PathType.MIN
