import time
from machine import I2C

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight_val = 0x08 # Backlight ON
        
        # wake up dance
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x03) # hal stands for Hardware abstraction layer (we speak their language since the lcd chipset is very old) excuse this part:)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        # this is how we wake up the lcd to listen to us
        self.hal_write_init_nibble(0x02) # Set 4-bit mode
        time.sleep_ms(1)
        # lcd_config
        self.display_func = 0x28 # function set mode
        self.display_control = 0x0C # display control (turn on the pixels, don't show underline [cursor off], don't blink the cursor)
        self.display_mode = 0x06 # typing rule: contract that when I type, move the cursor to the right.
        
        self.hal_write_command(self.display_func)
        self.hal_write_command(self.display_control) # Turn display ON
        self.hal_write_command(self.display_mode)
        self.clear()

    def hal_write_init_nibble(self, nibble):
        byte = (nibble << 4) | self.backlight_val
        # Write data with Enable High then Low
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        time.sleep_us(2) # Small delay
        self.i2c.writeto(self.i2c_addr, bytes([byte & ~0x04]))

    def hal_write_command(self, cmd):
        high = (cmd & 0xF0) | self.backlight_val
        low = ((cmd << 4) & 0xF0) | self.backlight_val
        self._write_byte(high)
        self._write_byte(low)

    def hal_write_data(self, data):
        high = (data & 0xF0) | self.backlight_val | 0x01
        low = ((data << 4) & 0xF0) | self.backlight_val | 0x01
        self._write_byte(high)
        self._write_byte(low)
        
    def _write_byte(self, byte):
        self.i2c.writeto(self.i2c_addr, bytes([byte | 0x04]))
        time.sleep_us(2)
        self.i2c.writeto(self.i2c_addr, bytes([byte & ~0x04]))
        
    def clear(self):
        self.hal_write_command(0x01)
        time.sleep_ms(2)

    def move_to(self, cursor_x, cursor_y):
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40 
        self.hal_write_command(0x80 | addr)

    def putstr(self, string):
        for char in string:
            self.hal_write_data(ord(char))
            
    def custom_char(self, location, char_map):
        self.hal_write_command(0x40 | (location << 3))
        for row in char_map:
            self.hal_write_data(row)
        self.hal_write_command(0x80)
        
    def show_char(self, location):
        self.hal_write_data(location)