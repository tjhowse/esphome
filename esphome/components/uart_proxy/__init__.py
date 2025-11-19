from logging import getLogger

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import (
    CONF_ID,
    CONF_RX_BUFFER_SIZE,
)
from esphome.components.uart import UARTComponent

_LOGGER = getLogger(__name__)

CODEOWNERS = ["@tjhowse"]
uart_proxy_ns = cg.esphome_ns.namespace("uart_proxy")
UartProxyComponent = uart_proxy_ns.class_("UartProxyComponent", UARTComponent, cg.Component)


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(UartProxyComponent),
            cv.Optional(CONF_RX_BUFFER_SIZE, default=1024): cv.validate_bytes,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)

)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_buffer_size(config[CONF_RX_BUFFER_SIZE]))


