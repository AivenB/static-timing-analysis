import pytest

from static_timing_analysis.timing_report import TimingReport


@pytest.fixture(scope="session")
def empty_report() -> TimingReport:
    return TimingReport.from_file("reports/empty.rpt")


@pytest.fixture(scope="session")
def simple_met_report() -> TimingReport:
    return TimingReport.from_file("reports/simple_met.rpt")


@pytest.fixture(scope="session")
def simple_violated_report() -> TimingReport:
    return TimingReport.from_file("reports/simple_violated.rpt")


@pytest.fixture(scope="session")
def mixed_report() -> TimingReport:
    return TimingReport.from_file("reports/mixed_paths.rpt")


@pytest.fixture(scope="session")
def full_report() -> TimingReport:
    return TimingReport.from_file("reports/timing_full.rpt")
