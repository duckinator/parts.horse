ATtiny85
========

The ATtiny25, ATtiny45, and ATtiny85 are 8-bit AVR microcontrollers.

They are all available in 8-pin DIP/SOIC (through-hole), 8-pin TSSOP (surface-mount), and 20-pin QFN/ML (surface-mount with 12 "do not connect" pins) form factors.

More details can be found at the following product pages on the Microchip website:

* `ATtiny25 <https://www.microchip.com/en-us/product/attiny25>`_
* `ATtiny45 <https://www.microchip.com/en-us/product/attiny45>`_
* `ATtiny85 <https://www.microchip.com/en-us/product/attiny85>`_

..
    {
      "name":           "ATtiny85",
      "datasheet":      "https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf",
      "details":        "https://www.microchip.com/wwwproducts/en/attiny85",
      "summary":        "8-bit AVR microcontroller with 8KB of program memory.",
      "style":          "DIP",
      "number_of_pins": 8,
      "tags": ["avr", "microcontroller", "8-bit"],
      "pins": [
        [["1", "PB5"], [" 8", "VCC"]],
        [["2", "PB3"], [" 7", "PB2"]],
        [["3", "PB4"], [" 6", "PB1"]],
        [["4", "GND"], [" 5", "PB0"]]
      ],
      "left_pin_functions": [
        ["1", "PB5", "PCINT5, ~RESET, ADC0, dW"],
        ["2", "PB3", "PCINT3,  XTAL1, CLKI, OC1B, ADC3"],
        ["3", "PB4", "PCINT4,  XTAL2, CLKO, OC1B, ADC2"],
        ["4", "GND", "Ground"]
      ],
      "right_pin_functions": [
        ["8", "VCC", "Positive supply voltage"],
        ["7", "PB2", "PCINT2, ADC1, INT0, SCK, SCL, T0, USCK"],
        ["6", "PB1", "PCINT1, AIN1,       DO, MISO, OC0B,  OC1A"],
        ["5", "PB0", "PCINT0, AINO, AREF, DI, MOSI, OC0A, ~OC1A, SDA"]
      ]
    }
