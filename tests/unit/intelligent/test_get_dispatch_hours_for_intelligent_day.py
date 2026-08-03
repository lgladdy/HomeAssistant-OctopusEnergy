from datetime import datetime, timedelta

from custom_components.octopus_energy.intelligent import get_dispatch_hours_for_intelligent_day
from custom_components.octopus_energy.api_client.intelligent_dispatches import SimpleIntelligentDispatchItem

# The intelligent day runs from noon on the day before `current` to noon on `current`'s day
current = datetime.strptime("2025-09-14T09:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
window_start = datetime.strptime("2025-09-13T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
window_end = datetime.strptime("2025-09-14T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")

def test_when_no_dispatches_then_returns_zero_hours():
  # Arrange
  dispatches = []

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0

def test_when_dispatch_is_entirely_before_window_then_it_is_not_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start - timedelta(hours=2),
      end=window_start - timedelta(hours=1)
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0

def test_when_dispatch_ends_exactly_at_window_start_then_it_is_not_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start - timedelta(hours=1),
      end=window_start
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0

def test_when_dispatch_starts_exactly_at_window_end_then_it_is_not_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_end,
      end=window_end + timedelta(hours=1)
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0

def test_when_single_dispatch_aligned_to_half_hours_then_it_returns_its_duration():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=8, minutes=30) # 20:30
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0.5

def test_when_dispatch_is_not_aligned_to_half_hours_then_it_is_rounded_to_the_nearest_half_hour_slot():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8, minutes=10), # 20:10
      end=window_start + timedelta(hours=8, minutes=20) # 20:20
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # Rounded down to 20:00 and up to 20:30
  assert result == 0.5

def test_when_dispatch_starts_before_window_but_ends_within_it_then_full_unclipped_duration_is_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start - timedelta(hours=1), # 11:00
      end=window_start + timedelta(hours=1) # 13:00
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # 11:00 - 13:00
  assert result == 2.0

def test_when_dispatches_do_not_overlap_then_hours_are_summed():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=8, minutes=30) # 20:30
    ),
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=10), # 22:00
      end=window_start + timedelta(hours=11) # 23:00
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # 0.5 (20:00 - 20:30) + 1.5 (22:00 - 23:00)
  assert result == 1.5

def test_when_dispatches_overlap_then_they_are_merged_and_only_counted_once():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=8, minutes=30) # 20:30
    ),
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8, minutes=15), # 20:15
      end=window_start + timedelta(hours=8, minutes=45) # 20:45
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # 20:00 - 21:00 (the second dispatch's end of 20:45 rounds up to 21:00)
  assert result == 1.0

def test_when_dispatch_extends_the_end_of_an_already_merged_dispatch_then_the_extended_duration_is_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=9) # 21:00
    ),
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8, minutes=30), # 20:30
      end=window_start + timedelta(hours=11, seconds=1) # 23:00:01
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # 20:00 - 23:30 (23:00 rounded up to the nearest half hour)
  assert result == 3.5

def test_when_dispatch_extends_the_start_of_an_already_merged_dispatch_then_the_extended_duration_is_counted():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=9), # 21:00
      end=window_start + timedelta(hours=10) # 22:00
    ),
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=9, minutes=30) # 21:30
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  # 20:00 - 22:00
  assert result == 2.0

def test_when_dispatch_is_shorter_than_half_an_hour_then_it_is_rounded_up_to_a_full_half_hour_slot():
  # Arrange
  dispatches = [
    SimpleIntelligentDispatchItem(
      start=window_start + timedelta(hours=8), # 20:00
      end=window_start + timedelta(hours=8, minutes=2) # 20:02
    )
  ]

  # Act
  result = get_dispatch_hours_for_intelligent_day(current, dispatches)

  # Assert
  assert result == 0.5
