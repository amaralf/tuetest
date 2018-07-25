import Adafruit_MCP4725

def volt():
    delta = 0
    dac1 = Adafruit_MCP4725.MCP4725()
    dac1.set_voltage(int(4096))
    dac2 = Adafruit_MCP4725.MCP4725(address=0x63, busnum=1)
    dac2.set_voltage(int(1024))
