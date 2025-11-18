#include "uart_proxy.h"
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
namespace uart_proxy {

static const char *const TAG = "uart.proxy";

void UartProxyComponent::setup() {
  ESP_LOGCONFIG(TAG, "Creating Proxy UART component");

}

void UartProxyComponent::write_array(const uint8_t *data, size_t len) {
    size_t space_left = this->max_buffer_size_ - this->bytes_.size();
    size_t to_write = std::min(len, space_left);
    for (size_t i = 0; i < to_write; i++) {
        this->bytes_.push(data[i]);
    }
}

bool UartProxyComponent::peek_byte(uint8_t *data) {
    if (this->bytes_.empty()) {
        return false;
    }
    *data = this->bytes_.front();
    return true;
}

bool UartProxyComponent::read_array(uint8_t *data, size_t len) {
    if (this->bytes_.empty()) {
        return false;
    }
    size_t to_read = std::min(len, this->bytes_.size());
    for (size_t i = 0; i < to_read; i++) {
        data[i] = this->bytes_.front();
        this->bytes_.pop();
    }
  return true;
}

}  // namespace uart
}  // namespace esphome

