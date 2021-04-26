from typing import Any

import cwa_qr
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

from custom_components.cwa_checkin_qr.const import DOMAIN

LOCATION_DESCRIPTION = "location_description"
ADDRESS = "address"
LOCATION_TYPE = "location_type"
DEFAULT_DURATION = "default_duration"

types = {
    "Retail": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_RETAIL,
    "Hospitality": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_FOOD_SERVICE,
    "Craft business": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_CRAFT,
    "Workplace": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_WORKPLACE,
    "Education facility": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION,
    "Public building": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING,
    "Other place": cwa_qr.lowlevel.LOCATION_TYPE_PERMANENT_OTHER,
    "Cultural event": cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT,
    "Club activities": cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY,
    "Private party": cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT,
    "Religious service": cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE,
    "Other event": cwa_qr.lowlevel.LOCATION_TYPE_TEMPORARY_OTHER,
    "Other": cwa_qr.lowlevel.LOCATION_TYPE_UNSPECIFIED,
}


class CWAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(
            self, user_input: dict[str, Any] = None
    ) -> dict[str, Any]:
        if user_input is not None:
            user_input[LOCATION_TYPE] = types[user_input[LOCATION_TYPE]]
            return self.async_create_entry(
                title=user_input[LOCATION_DESCRIPTION],
                data=user_input
            )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
                vol.Required(LOCATION_DESCRIPTION): vol.All(cv.string, vol.Length(max=100)),
                vol.Required(ADDRESS): vol.All(cv.string, vol.Length(max=100)),
                vol.Required(LOCATION_TYPE, default="Other"): vol.In(list(types.keys())),
                #vol.Inclusive("start_date_time", "dates"): vol.Datetime,
                #vol.Inclusive("end_date_time", "dates"): vol.Datetime,
                vol.Required(DEFAULT_DURATION, default=60): cv.positive_int
            })
        )
