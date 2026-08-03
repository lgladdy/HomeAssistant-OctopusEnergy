from datetime import datetime, timedelta

from custom_components.octopus_energy.intelligent import is_within_intelligent_cap
from custom_components.octopus_energy.api_client.intelligent_dispatches import SimpleIntelligentDispatchItem

# The intelligent day runs from noon on the day before `current` to noon on `current`'s day
current = datetime.strptime("2025-09-14T09:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
window_start = datetime.strptime("2025-09-13T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")

def test_when_no_dispatches_then_it_is_within_cap():
  # Arrange
  dispatches = []

  # Act
  result = is_within_intelligent_cap(current, dispatches)

  # Assert
  assert result is True

def test_when_dispatch_hours_are_well_under_six_then_it_is_within_cap():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start,
      end=window_start + timedelta(hours=1)
    )
  ]

  # Act
  result = is_within_intelligent_cap(current, dispatches)

  # Assert
  assert result is True

def test_when_dispatch_hours_equal_six_then_it_is_within_cap():
  # Arrange
  # Start/end aligned to the half hour so rounding doesn't shift the total away from 6
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(minutes=30),
      end=window_start + timedelta(hours=6, minutes=30)
    )
  ]

  # Act
  result = is_within_intelligent_cap(current, dispatches)

  # Assert
  assert result is True

def test_when_dispatch_hours_exceed_six_then_it_is_not_within_cap():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(minutes=30),
      end=window_start + timedelta(hours=6, minutes=31)
    )
  ]

  # Act
  result = is_within_intelligent_cap(current, dispatches)

  # Assert
  assert result is False

def test_when_dispatch_hours_are_outside_the_intelligent_day_window_then_they_are_ignored():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start - timedelta(hours=10),
      end=window_start - timedelta(hours=5)
    )
  ]

  # Act
  result = is_within_intelligent_cap(current, dispatches)

  # Assert
  assert result is True
