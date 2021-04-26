import io

import cwa_qr
from homeassistant.components.camera import Camera

from custom_components.cwa_checkin_qr import config_flow


async def async_setup_entry(hass, config_entry, async_add_entities):
    cameras = [
        CWAQRCamera(
            hass,
            config_entry.data
        )
    ]

    async_add_entities(cameras)


def to_png(image):
    png_image = io.BytesIO()
    image.save(png_image, format="png")
    png_image.seek(0)
    data = png_image.read()
    png_image.close()
    return data


class CWAQRCamera(Camera):
    def __init__(self, hass, config):
        super().__init__()
        self.config = config
        self._current_image = None

    def generate_image(self):
        event_description = cwa_qr.CwaEventDescription()
        event_description.location_description = self.config[config_flow.LOCATION_DESCRIPTION]
        event_description.location_address = self.config[config_flow.ADDRESS]
        # event_description.start_date_time = datetime(2021, 4, 25, 8, 0).astimezone(timezone.utc)
        # event_description.end_date_time = datetime(2021, 4, 25, 18, 0).astimezone(timezone.utc)
        event_description.location_type = self.config[config_flow.LOCATION_TYPE]
        event_description.default_check_in_length_in_minutes = self.config[config_flow.DEFAULT_DURATION]
        qr = cwa_qr.generate_qr_code(event_description)

        return to_png(qr.make_image())

    async def async_camera_image(self):
        if self._current_image is None:
            self._current_image = self.generate_image()
        return self._current_image

    @property
    def name(self):
        """Return the name of this camera."""
        return self.config[config_flow.LOCATION_DESCRIPTION]
