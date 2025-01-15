from struct import unpack
from micropython import const
from machine import I2C

_ADXL345_DEFAULT_ADDRESS: int = const(0x53)
# Conversion factors
_ADXL345_MG2G_MULTIPLIER: float = 0.004  # 4mg per lsb
_STANDARD_GRAVITY: float = 9.80665  # earth standard gravity

_REG_DEVID: int = const(0x00)  # Device ID
_REG_THRESH_TAP: int = const(0x1D)  # Tap threshold
_REG_OFSX: int = const(0x1E)  # X-axis offset
_REG_OFSY: int = const(0x1F)  # Y-axis offset
_REG_OFSZ: int = const(0x20)  # Z-axis offset
_REG_DUR: int = const(0x21)  # Tap duration
_REG_LATENT: int = const(0x22)  # Tap latency
_REG_WINDOW: int = const(0x23)  # Tap window
_REG_THRESH_ACT: int = const(0x24)  # Activity threshold
_REG_THRESH_INACT: int = const(0x25)  # Inactivity threshold
_REG_TIME_INACT: int = const(0x26)  # Inactivity time
_REG_ACT_INACT_CTL: int = const(0x27)  # Axis enable control for [in]activity detection
_REG_THRESH_FF: int = const(0x28)  # Free-fall threshold
_REG_TIME_FF: int = const(0x29)  # Free-fall time
_REG_TAP_AXES: int = const(0x2A)  # Axis control for single/double tap
_REG_ACT_TAP_STATUS: int = const(0x2B)  # Source for single/double tap
_REG_BW_RATE: int = const(0x2C)  # Data rate and power mode control
_REG_POWER_CTL: int = const(0x2D)  # Power-saving features control
_REG_INT_ENABLE: int = const(0x2E)  # Interrupt enable control
_REG_INT_MAP: int = const(0x2F)  # Interrupt mapping control
_REG_INT_SOURCE: int = const(0x30)  # Source of interrupts
_REG_DATA_FORMAT: int = const(0x31)  # Data format control
_REG_DATAX0: int = const(0x32)  # X-axis data 0
_REG_DATAX1: int = const(0x33)  # X-axis data 1
_REG_DATAY0: int = const(0x34)  # Y-axis data 0
_REG_DATAY1: int = const(0x35)  # Y-axis data 1
_REG_DATAZ0: int = const(0x36)  # Z-axis data 0
_REG_DATAZ1: int = const(0x37)  # Z-axis data 1
_REG_FIFO_CTL: int = const(0x38)  # FIFO control
_REG_FIFO_STATUS: int = const(0x39)  # FIFO status
_INT_SINGLE_TAP: int = const(0b01000000)  # SINGLE_TAP bit
_INT_DOUBLE_TAP: int = const(0b00100000)  # DOUBLE_TAP bit
_INT_ACT: int = const(0b00010000)  # ACT bit
_INT_INACT: int = const(0b00001000)  # INACT bit
_INT_FREE_FALL: int = const(0b00000100)  # FREE_FALL  bit


class DataRate:  # pylint: disable=too-few-public-methods
    """An enum-like class representing the possible data rates.

    Possible values are:

    - ``DataRate.RATE_3200_HZ``
    - ``DataRate.RATE_1600_HZ``
    - ``DataRate.RATE_800_HZ``
    - ``DataRate.RATE_400_HZ``
    - ``DataRate.RATE_200_HZ``
    - ``DataRate.RATE_100_HZ``
    - ``DataRate.RATE_50_HZ``
    - ``DataRate.RATE_25_HZ``
    - ``DataRate.RATE_12_5_HZ``
    - ``DataRate.RATE_6_25HZ``
    - ``DataRate.RATE_3_13_HZ``
    - ``DataRate.RATE_1_56_HZ``
    - ``DataRate.RATE_0_78_HZ``
    - ``DataRate.RATE_0_39_HZ``
    - ``DataRate.RATE_0_20_HZ``
    - ``DataRate.RATE_0_10_HZ``

    """

    RATE_3200_HZ: int = const(0b1111)  # 1600Hz Bandwidth   140mA IDD
    RATE_1600_HZ: int = const(0b1110)  # 800Hz Bandwidth    90mA IDD
    RATE_800_HZ: int = const(0b1101)  # 400Hz Bandwidth   140mA IDD
    RATE_400_HZ: int = const(0b1100)  # 200Hz Bandwidth   140mA IDD
    RATE_200_HZ: int = const(0b1011)  # 100Hz Bandwidth   140mA IDD
    RATE_100_HZ: int = const(0b1010)  # 50Hz Bandwidth   140mA IDD
    RATE_50_HZ: int = const(0b1001)  # 25Hz Bandwidth    90mA IDD
    RATE_25_HZ: int = const(0b1000)  # 12.5Hz Bandwidth    60mA IDD
    RATE_12_5_HZ: int = const(0b0111)  # 6.25Hz Bandwidth    50mA IDD
    RATE_6_25HZ: int = const(0b0110)  # 3.13Hz Bandwidth    45mA IDD
    RATE_3_13_HZ: int = const(0b0101)  # 1.56Hz Bandwidth    40mA IDD
    RATE_1_56_HZ: int = const(0b0100)  # 0.78Hz Bandwidth    34mA IDD
    RATE_0_78_HZ: int = const(0b0011)  # 0.39Hz Bandwidth    23mA IDD
    RATE_0_39_HZ: int = const(0b0010)  # 0.20Hz Bandwidth    23mA IDD
    RATE_0_20_HZ: int = const(0b0001)  # 0.10Hz Bandwidth    23mA IDD
    RATE_0_10_HZ: int = const(0b0000)  # 0.05Hz Bandwidth    23mA IDD (default value)


class Range:  # pylint: disable=too-few-public-methods
    """An enum-like class representing the possible measurement ranges in +/- G.

    Possible values are:

    - ``Range.RANGE_16_G``
    - ``Range.RANGE_8_G``
    - ``Range.RANGE_4_G``
    - ``Range.RANGE_2_G``

    """

    RANGE_16_G: int = const(0b11)  # +/- 16g
    RANGE_8_G: int = const(0b10)  # +/- 8g
    RANGE_4_G: int = const(0b01)  # +/- 4g
    RANGE_2_G: int = const(0b00)  # +/- 2g (default value)




class ADXL345:
    def __init__(self, i2c: I2C, address: int = _ADXL345_DEFAULT_ADDRESS):
        self._i2c = i2c
        self._buffer = bytearray(6)
        self._wbuffer = bytearray(1)
        self._write_register_byte(_REG_POWER_CTL, 0x08)
        self._write_register_byte(_REG_INT_ENABLE, 0x0)
        
        self._enabled_interrupts = {}
        self._event_status = {}
        
    @property
    def acceleration(self) -> Tuple[int, int, int]:
        """The x, y, z acceleration values returned in a 3-tuple in :math:`m / s ^ 2`"""
        x, y, z = unpack("<hhh", self._read_register(_REG_DATAX0, 6))
        x = x * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        y = y * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        z = z * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        return x, y, z
    
    @property
    def raw_x(self) -> int:
        return unpack("<h", self._read_register(_REG_DATAX0, 2))[0]
    
    @property
    def raw_y(self) -> int:
        return unpack("<h", self._read_register(_REG_DATAY0, 2))[0]
    
    @property
    def raw_z(self) -> int:
        return unpack("<h", self._read_register(_REG_DATAZ0, 2))[0]
    
    @property
    def data_rate(self) -> int:
        """The data rate of the sensor."""
        rate_register = self._read_register_unpacked(_REG_BW_RATE)
        return rate_register & 0x0F

    @data_rate.setter
    def data_rate(self, val: int) -> None:
        self._write_register_byte(_REG_BW_RATE, val)

    @property
    def range(self) -> int:
        """The measurement range of the sensor."""
        range_register = self._read_register_unpacked(_REG_DATA_FORMAT)
        return range_register & 0x03

    @range.setter
    def range(self, val: int) -> None:
        # read the current value of the data format register
        format_register = self._read_register_unpacked(_REG_DATA_FORMAT)

        # clear the bottom 4 bits and update the data rate
        format_register &= ~0x0F
        format_register |= val

        # Make sure that the FULL-RES bit is enabled for range scaling
        format_register |= 0x08

        # write the updated values
        self._write_register_byte(_REG_DATA_FORMAT, format_register)

    @property
    def offset(self) -> Tuple[int, int, int]:
        """
        The x, y, z offsets as a tuple of raw count values.

        See offset_calibration example for usage.
        """
        x_offset, y_offset, z_offset = unpack("<bbb", self._read_register(_REG_OFSX, 3))
        return x_offset, y_offset, z_offset

    @offset.setter
    def offset(self, val: Tuple[int, int, int]) -> None:
        x_offset, y_offset, z_offset = val
        self._write_register_byte(_REG_OFSX, x_offset)
        self._write_register_byte(_REG_OFSY, y_offset)
        self._write_register_byte(_REG_OFSZ, z_offset)

    
    def _read_clear_interrupt_source(self) -> int:
        return self._read_register_unpacked(_REG_INT_SOURCE)
    
    def _read_register_unpacked(self, register: int) -> int:
        return unpack("<b", self._read_register(register, 1))[0]
        
    def _read_register(self, register: int, length: int) -> int:
        self._wbuffer[0] = register & 0xFF
        #with self._i2c as i2c:
        self._i2c.writeto_mem(_ADXL345_DEFAULT_ADDRESS, register, self._wbuffer)
        #self._i2c.readinto(self._buffer, start=0, end=length)
        self._buffer = self._i2c.readfrom(_ADXL345_DEFAULT_ADDRESS, register, length)              
        return self._buffer[0:length]

    def _write_register_byte(self, register: int, value: int) -> None:
        #self._wbuffer[0] = register & 0xFF
        #self._wbuffer[1] = value & 0xFF
        self._wbuffer[0] = value & 0xFF
        #while self._i2c as i2c:
        #	i2c.write(self.buffer, start=0, end=2)
        self._i2c.writeto_mem(_ADXL345_DEFAULT_ADDRESS, register, self._wbuffer)
