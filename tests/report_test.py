import pytest
from src import report


@pytest.fixture
def report_1():
    '''
    Create successful report
    '''
    report_name = report.create_new(1)
    report.update_successful(report_name)
    return report_name


@pytest.fixture
def report_2():
    '''
    Create unsucessful report
    '''
    report_name = report.create_new(2)
    report.update_unsuccessful(report_name, "unknown error")
    return report_name


@pytest.fixture
def clear():
    '''
    Clear reports
    '''
    report.clear_reports()


def test_create_new(clear):
    '''
    Test return of create_new
    '''
    result = report.create_new(100)
    assert type(result) is str
    assert result == 'reports/invoice_100_report.json'


def test_update_successful(clear):
    '''
    Test return type of update_succesful
    '''
    report_name = report.create_new(200)
    report.update_successful(report_name)


def test_update_unsuccessful(clear):
    '''
    Test return type of update_unsuccesful
    '''
    report_name = report.create_new(200)
    report.update_unsuccessful(report_name, "unknown error")


def test_return_reports(clear, report_1, report_2):
    '''
    Test return type of return_reports
    '''
    result = report.return_reports()
    assert type(result) is list
    assert result == [{"invoice_id": 1, "status": "success", "error": "none"},
                      {"invoice_id": 2, "status": "unsuccessful", "error": "unknown error"}]


def test_clear_reports():
    '''
    Test return type of clear_reports
    '''
    report.clear_reports()
