#include "uart_component_proxy.h"
#include "esphome/core/application.h"
#include "esphome/core/defines.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <sys/ioctl.h>

#ifdef USE_LOGGER
#include "esphome/components/logger/logger.h"
#endif

namespace esphome {
namespace uart {

static const char *const TAG = "uart.proxy";

ProxyUartComponent::~ProxyUartComponent() {
    this->bytes_.clear();
}

void ProxyUartComponent::setup() {
  ESP_LOGCONFIG(TAG, "Creating Proxy UART component");
}

void ProxyUartComponent::write_array(const uint8_t *data, size_t len) {
    size_t space_left = this->max_buffer_size_ - this->bytes_.size();
    size_t to_write = std::min(len, space_left);
    for (size_t i = 0; i < to_write; i++) {
        this->bytes_.push(data[i]);
    }
}

bool ProxyUartComponent::peek_byte(uint8_t *data) {
    if (this->bytes_.empty()) {
        return false;
    }
    *data = this->bytes_.front();
    return true;
}

bool ProxyUartComponent::read_array(uint8_t *data, size_t len) {
    if (this->bytes_.empty()) {
        return false;
    }
    size_t to_read = std::min(len, this->bytes_.size());
    for (size_t i = 0; i < to_read; i++) {
        data[i] = this->bytes_.front();
        this->bytes_.pop();
    }
#ifdef USE_UART_DEBUGGER
    for (size_t i = 0; i < to_read; i++) {
        this->debug_callback_.call(UART_DIRECTION_RX, data[i]);
    }
#endif
  return true;
}

}  // namespace uart
}  // namespace esphome

