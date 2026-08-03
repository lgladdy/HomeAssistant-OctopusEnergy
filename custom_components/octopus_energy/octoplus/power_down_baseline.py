import logging

from .saving_session_baseline import OctopusEnergySavingSessionBaseline

_LOGGER = logging.getLogger(__name__)

class OctopusEnergyPowerDownBaseline(OctopusEnergySavingSessionBaseline):
  """Sensor for determining the baseline for the current or next power down session."""

  @property
  def unique_id(self):
    """The id of the sensor."""
    return f"octopus_energy_electricity_{self._serial_number}_{self._mpan}{self._export_id_addition}_octoplus_power_down_baseline"

  @property
  def name(self):
    """Name of the sensor."""
    return f"Octoplus Power Down Baseline {self._export_name_addition}Electricity ({self._serial_number}/{self._mpan})"
