#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"
#include "esphome/components/uart/uart_component.h"

#include <queue>

namespace esphome {
namespace uart_proxy {

class UartProxyComponent : public uart::UARTComponent, public Component {
 public:
  // Provide an inline defaulted destructor to ensure the vtable is emitted.
  ~UartProxyComponent() override = default;
  void setup() override;
  void write_array(const uint8_t *data, size_t len) override;
  bool peek_byte(uint8_t *data) override;
  bool read_array(uint8_t *data, size_t len) override;
  int available() override { return this->bytes_.size(); }
  void flush() override { this->bytes_ = std::queue<uint8_t>(); }
  void set_buffer_size(size_t size) { this->max_buffer_size_ = size; };

 protected:
  std::queue<uint8_t> bytes_{};
  size_t max_buffer_size_{1024};
  void check_logger_conflict() override {}
};

}  // namespace uart
}  // namespace esphome

