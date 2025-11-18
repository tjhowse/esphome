from logging import getLogger

from esphome import automation, pins
import esphome.codegen as cg
from esphome.config_helpers import filter_source_files_from_platform
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_RX_BUFFER_SIZE,
)
from esphome.core import CORE, ID
import esphome.final_validate as fv
from esphome.yaml_util import make_data_base
from esphome.components.uart import UARTComponent

_LOGGER = getLogger(__name__)

CODEOWNERS = ["@tjhowse"]
uart_proxy_ns = cg.esphome_ns.namespace("uart_proxy")
UartProxyComponent = uart_proxy_ns.class_("UartProxyComponent", UARTComponent, cg.Component)

def validate_rx_buffer_size(config):
    if CORE.is_esp32:
        # ESP32 UART hardware FIFO is 128 bytes (LP UART is 16 bytes, but we use 128 as safe minimum)
        # rx_buffer_size must be greater than the hardware FIFO length
        min_buffer_size = 128
        if config[CONF_RX_BUFFER_SIZE] <= min_buffer_size:
            _LOGGER.warning(
                "UART rx_buffer_size (%d bytes) is too small and must be greater than the hardware "
                "FIFO size (%d bytes). The buffer size will be automatically adjusted at runtime.",
                config[CONF_RX_BUFFER_SIZE],
                min_buffer_size,
            )
    return config

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(UartProxyComponent),
            cv.Optional(CONF_RX_BUFFER_SIZE, default=256): cv.validate_bytes,
        }
    ).extend(cv.COMPONENT_SCHEMA),
    validate_rx_buffer_size,
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_rx_buffer_size(config[CONF_RX_BUFFER_SIZE]))


