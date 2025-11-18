from logging import getLogger

from esphome import automation, pins
import esphome.codegen as cg
from esphome.config_helpers import filter_source_files_from_platform
import esphome.config_validation as cv
from esphome.const import (
    CONF_AFTER,
    CONF_BAUD_RATE,
    CONF_BYTES,
    CONF_DATA,
    CONF_DEBUG,
    CONF_DELIMITER,
    CONF_DIRECTION,
    CONF_DUMMY_RECEIVER,
    CONF_DUMMY_RECEIVER_ID,
    CONF_FLOW_CONTROL_PIN,
    CONF_ID,
    CONF_INVERT,
    CONF_LAMBDA,
    CONF_NUMBER,
    CONF_PORT,
    CONF_RX_BUFFER_SIZE,
    CONF_RX_PIN,
    CONF_SEQUENCE,
    CONF_TIMEOUT,
    CONF_TRIGGER_ID,
    CONF_TX_PIN,
    CONF_UART_ID,
    PLATFORM_HOST,
    PlatformFramework,
)
from esphome.core import CORE, ID
import esphome.final_validate as fv
from esphome.yaml_util import make_data_base

_LOGGER = getLogger(__name__)

CODEOWNERS = ["@esphome/core"]

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
            cv.Optional(CONF_RX_BUFFER_SIZE, default=256): cv.validate_bytes,
        }
    ).extend(cv.COMPONENT_SCHEMA),
    validate_rx_buffer_size,
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.set_baud_rate(config[CONF_BAUD_RATE]))

    cg.add(var.set_rx_buffer_size(config[CONF_RX_BUFFER_SIZE]))


