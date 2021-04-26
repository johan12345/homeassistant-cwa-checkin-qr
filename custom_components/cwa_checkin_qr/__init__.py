from homeassistant import core
from homeassistant.config_entries import ConfigEntry


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Corona Warn-App check-in QR code component."""
    return True


async def async_setup_entry(hass: core.HomeAssistant, config_entry: ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "camera")
    )