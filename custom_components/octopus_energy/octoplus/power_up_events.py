import logging

from homeassistant.core import HomeAssistant

from ..const import EVENT_ALL_POWER_UP_SESSIONS
from .free_electricity_sessions_events import OctopusEnergyOctoplusFreeElectricitySessionEvents

_LOGGER = logging.getLogger(__name__)

class OctopusEnergyOctoplusPowerUpEvents(OctopusEnergyOctoplusFreeElectricitySessionEvents):
  """Sensor for displaying the upcoming power up events."""

  _attr_translation_key = "power_up_sessions"

  def __init__(self, hass: HomeAssistant, account_id: str):
    """Init sensor."""
    super().__init__(hass, account_id)

    self._attr_event_types = [EVENT_ALL_POWER_UP_SESSIONS]

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"octopus_energy_{self._account_id}_octoplus_power_up_events"

  @property
  def name(self):
    """Name of the sensor."""
    return f"Octoplus Power Up Events ({self._account_id})"
