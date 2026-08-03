import logging

from homeassistant.core import HomeAssistant

from ..const import EVENT_ALL_POWER_DOWN_SESSIONS
from ..api_client import OctopusEnergyApiClient
from .saving_sessions_events import OctopusEnergyOctoplusSavingSessionEvents

_LOGGER = logging.getLogger(__name__)

class OctopusEnergyOctoplusPowerDownEvents(OctopusEnergyOctoplusSavingSessionEvents):
  """Sensor for displaying the upcoming power down events."""

  _attr_translation_key = "power_down_sessions"

  def __init__(self, hass: HomeAssistant, client: OctopusEnergyApiClient, account_id: str):
    """Init sensor."""
    super().__init__(hass, client, account_id)

    self._attr_event_types = [EVENT_ALL_POWER_DOWN_SESSIONS]

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"octopus_energy_{self._account_id}_octoplus_power_down_events"

  @property
  def name(self):
    """Name of the sensor."""
    return f"Octoplus Power Down Events ({self._account_id})"
