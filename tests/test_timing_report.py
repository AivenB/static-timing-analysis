from static_timing_analysis.timing_path import PathType, SlackStatus
from static_timing_analysis.timing_report import TimingReport


class TestEmptyReport:
    def test_no_paths(self, empty_report: TimingReport) -> None:
        assert len(empty_report.paths) == 0


class TestSimpleMetReport:
    def test_one_path(self, simple_met_report: TimingReport) -> None:
        assert len(simple_met_report.paths) == 1

    def test_fields(self, simple_met_report: TimingReport) -> None:
        path = simple_met_report.paths[0]
        assert path.startpoint == "reg_a"
        assert path.endpoint == "reg_b"
        assert path.path_group == "clk"
        assert path.path_type == PathType.MAX
        assert path.arrival_time == 5.0
        assert path.required_time == 10.0
        assert path.slack == 5.0
        assert path.status == SlackStatus.MET


class TestSimpleViolatedReport:
    def test_one_path(self, simple_violated_report: TimingReport) -> None:
        assert len(simple_violated_report.paths) == 1

    def test_status_and_slack(self, simple_violated_report: TimingReport) -> None:
        path = simple_violated_report.paths[0]
        assert path.status == SlackStatus.VIOLATED
        assert path.slack == -5.0


class TestMixedReport:
    def test_four_paths(self, mixed_report: TimingReport) -> None:
        assert len(mixed_report.paths) == 4

    def test_startpoints(self, mixed_report: TimingReport) -> None:
        startpoints = [p.startpoint for p in mixed_report.paths]
        assert "reg_min_violated" in startpoints
        assert "reg_max_violated" in startpoints
        assert "reg_min_met" in startpoints
        assert "reg_max_met" in startpoints

    def test_groups(self, mixed_report: TimingReport) -> None:
        groups = {p.path_group for p in mixed_report.paths}
        assert groups == {"clk_group", "other_group"}

    def test_statuses(self, mixed_report: TimingReport) -> None:
        statuses = [p.status for p in mixed_report.paths]
        assert statuses.count(SlackStatus.MET) == 2
        assert statuses.count(SlackStatus.VIOLATED) == 2

    def test_path_types(self, mixed_report: TimingReport) -> None:
        types = [p.path_type for p in mixed_report.paths]
        assert types.count(PathType.MIN) == 2
        assert types.count(PathType.MAX) == 2


class TestFullReport:
    def test_path_count(self, full_report: TimingReport) -> None:
        assert len(full_report.paths) == 102

    def test_path_group(self, full_report: TimingReport) -> None:
        groups = {p.path_group for p in full_report.paths}
        assert groups == {"core_clock"}


class TestFromString:
    def test_matches_from_file(self, simple_met_report: TimingReport) -> None:
        with open("reports/simple_met.rpt", encoding="utf-8") as f:
            text = f.read()
        report = TimingReport.from_string(text)
        assert len(report.paths) == len(simple_met_report.paths)
        assert report.paths[0].slack == simple_met_report.paths[0].slack


class TestFilter:
    def test_filter_by_status(self, mixed_report: TimingReport) -> None:
        violated = mixed_report.filter(status=SlackStatus.VIOLATED)
        assert len(violated) == 2
        assert all(p.status == SlackStatus.VIOLATED for p in violated)

    def test_filter_by_type(self, mixed_report: TimingReport) -> None:
        max_paths = mixed_report.filter(path_type=PathType.MAX)
        assert len(max_paths) == 2
        assert all(p.path_type == PathType.MAX for p in max_paths)

    def test_filter_by_group(self, mixed_report: TimingReport) -> None:
        paths = mixed_report.filter(group="clk_group")
        assert len(paths) == 2
        assert all(p.path_group == "clk_group" for p in paths)

    def test_combined_filter(self, mixed_report: TimingReport) -> None:
        paths = mixed_report.filter(status=SlackStatus.VIOLATED, path_type=PathType.MIN)
        assert len(paths) == 1
        assert paths[0].startpoint == "reg_min_violated"

    def test_no_filters_returns_all(self, mixed_report: TimingReport) -> None:
        assert len(mixed_report.filter()) == 4

    def test_filter_no_match(self, mixed_report: TimingReport) -> None:
        assert mixed_report.filter(group="nonexistent") == []
