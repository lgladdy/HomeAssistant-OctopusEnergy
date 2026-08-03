import logging

from .saving_sessions_calendar import OctopusEnergySavingSessionsCalendar

_LOGGER = logging.getLogger(__name__)

class OctopusEnergyPowerDownCalendar(OctopusEnergySavingSessionsCalendar):
  """Sensor for power down calendar"""

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"octopus_energy_{self._account_id}_octoplus_power_down"

  @property
  def name(self):
    """Name of the sensor."""
    return f"Octoplus Power Down ({self._account_id})"
