"""Config flow for Baby Monitor integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    ATTR_BABY_NAME,
    CONF_MIN_DIAPERS_PER_DAY,
    CONF_MIN_WET_DIAPERS_PER_DAY,
    CONF_MIN_FEEDINGS_PER_DAY,
    CONF_MIN_SLEEP_HOURS_PER_DAY,
    CONF_TARGET_TUMMY_TIME_MINUTES,
    CONF_FEEDING_REMINDER_HOURS,
    CONF_DIAPER_REMINDER_HOURS,
    DEFAULT_MIN_DIAPERS_PER_DAY,
    DEFAULT_MIN_WET_DIAPERS_PER_DAY,
    DEFAULT_MIN_FEEDINGS_PER_DAY,
    DEFAULT_MIN_SLEEP_HOURS_PER_DAY,
    DEFAULT_TARGET_TUMMY_TIME_MINUTES,
    DEFAULT_FEEDING_REMINDER_HOURS,
    DEFAULT_DIAPER_REMINDER_HOURS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_BABY_NAME): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Baby Monitor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                baby_name = user_input[ATTR_BABY_NAME]
                
                # Set unique ID based on baby name
                await self.async_set_unique_id(baby_name.lower().replace(" ", "_"))
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"Baby Monitor - {baby_name}",
                    data=user_input,
                    options={
                        CONF_MIN_DIAPERS_PER_DAY: DEFAULT_MIN_DIAPERS_PER_DAY,
                        CONF_MIN_WET_DIAPERS_PER_DAY: DEFAULT_MIN_WET_DIAPERS_PER_DAY,
                        CONF_MIN_FEEDINGS_PER_DAY: DEFAULT_MIN_FEEDINGS_PER_DAY,
                        CONF_MIN_SLEEP_HOURS_PER_DAY: DEFAULT_MIN_SLEEP_HOURS_PER_DAY,
                        CONF_TARGET_TUMMY_TIME_MINUTES: DEFAULT_TARGET_TUMMY_TIME_MINUTES,
                        CONF_FEEDING_REMINDER_HOURS: DEFAULT_FEEDING_REMINDER_HOURS,
                        CONF_DIAPER_REMINDER_HOURS: DEFAULT_DIAPER_REMINDER_HOURS,
                    }
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidBabyName:
                errors[ATTR_BABY_NAME] = "invalid_baby_name"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Baby Monitor."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        baby_name = self.config_entry.data.get(ATTR_BABY_NAME, "Baby")

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_MIN_DIAPERS_PER_DAY,
                    default=options.get(CONF_MIN_DIAPERS_PER_DAY, DEFAULT_MIN_DIAPERS_PER_DAY),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=20)),
                vol.Optional(
                    CONF_MIN_WET_DIAPERS_PER_DAY,
                    default=options.get(CONF_MIN_WET_DIAPERS_PER_DAY, DEFAULT_MIN_WET_DIAPERS_PER_DAY),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=15)),
                vol.Optional(
                    CONF_MIN_FEEDINGS_PER_DAY,
                    default=options.get(CONF_MIN_FEEDINGS_PER_DAY, DEFAULT_MIN_FEEDINGS_PER_DAY),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=20)),
                vol.Optional(
                    CONF_MIN_SLEEP_HOURS_PER_DAY,
                    default=options.get(CONF_MIN_SLEEP_HOURS_PER_DAY, DEFAULT_MIN_SLEEP_HOURS_PER_DAY),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
                vol.Optional(
                    CONF_TARGET_TUMMY_TIME_MINUTES,
                    default=options.get(CONF_TARGET_TUMMY_TIME_MINUTES, DEFAULT_TARGET_TUMMY_TIME_MINUTES),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=120)),
                vol.Optional(
                    CONF_FEEDING_REMINDER_HOURS,
                    default=options.get(CONF_FEEDING_REMINDER_HOURS, DEFAULT_FEEDING_REMINDER_HOURS),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=12)),
                vol.Optional(
                    CONF_DIAPER_REMINDER_HOURS,
                    default=options.get(CONF_DIAPER_REMINDER_HOURS, DEFAULT_DIAPER_REMINDER_HOURS),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=12)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={"baby_name": baby_name},
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidBabyName(HomeAssistantError):
    """Error to indicate there is invalid baby name."""