from datetime import datetime
import pytest

from custom_components.octopus_energy.utils.datetime import round_down_to_nearest_half_hour

@pytest.mark.parametrize("dt,expected",[
  (datetime.strptime("2023-07-14T10:00:00+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:00:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:00:00.500000+01:00", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.strptime("2023-07-14T10:00:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:15:30+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:00:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:29:59+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:00:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:30:00+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:30:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:45:15+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:30:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
  (datetime.strptime("2023-07-14T10:59:59+01:00", "%Y-%m-%dT%H:%M:%S%z"), datetime.strptime("2023-07-14T10:30:00+01:00", "%Y-%m-%dT%H:%M:%S%z")),
])
def test_when_datetime_provided_then_rounded_down_to_nearest_half_hour(dt, expected):
  # Act
  result = round_down_to_nearest_half_hour(dt)

  # Assert
  assert result == expected
