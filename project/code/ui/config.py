
class LcdConfig(object):
    """LCD屏幕参数配置"""
    
    LCD_INIT_DATA = bytes(
        (
            0, 0, 0x11,
            2, 0, 120,
            0, 1, 0x36,
            1, 1, 0x00,
            0, 1, 0x3A,
            1, 1, 0x05,
            0, 5, 0xB2,
            1, 1, 0x05,
            1, 1, 0x05,
            1, 1, 0x00,
            1, 1, 0x33,
            1, 1, 0x33,
            0, 1, 0xB7,
            1, 1, 0x75,
            0, 1, 0xBB,
            1, 1, 0x22,
            0, 1, 0xC0,
            1, 1, 0x2C,
            0, 1, 0xC2,
            1, 1, 0x01,
            0, 1, 0xC3,
            1, 1, 0x13,
            0, 1, 0xC4,
            1, 1, 0x20,
            0, 1, 0xC6,
            1, 1, 0x11,
            0, 2, 0xD0,
            1, 1, 0xA4,
            1, 1, 0xA1,
            0, 1, 0xD6,
            1, 1, 0xA1,
            0, 14, 0xE0,
            1, 1, 0xD0,
            1, 1, 0x05,
            1, 1, 0x0A,
            1, 1, 0x09,
            1, 1, 0x08,
            1, 1, 0x05,
            1, 1, 0x2E,
            1, 1, 0x44,
            1, 1, 0x45,
            1, 1, 0x0F,
            1, 1, 0x17,
            1, 1, 0x16,
            1, 1, 0x2B,
            1, 1, 0x33,
            0, 14, 0xE1,
            1, 1, 0xD0,
            1, 1, 0x05,
            1, 1, 0x0A,
            1, 1, 0x09,
            1, 1, 0x08,
            1, 1, 0x05,
            1, 1, 0x2E,
            1, 1, 0x43,
            1, 1, 0x45,
            1, 1, 0x0F,
            1, 1, 0x16,
            1, 1, 0x16,
            1, 1, 0x2B,
            1, 1, 0x33,
            0, 0, 0x29,
            0, 0, 0x21
        )
    )

    LCD_INVALID = bytes(
        (
            0, 4, 0x2a,
            1, 1, 0xf0,
            1, 1, 0xf1,
            1, 1, 0xE0,
            1, 1, 0xE1,
            0, 4, 0x2b,
            1, 1, 0xf2,
            1, 1, 0xf3,
            1, 1, 0xE2,
            1, 1, 0xE3,
            0, 0, 0x2c,
        )
    )

    LCD_DISPLAY_OFF = bytes(
        (
            0, 0, 0x11,
            2, 0, 20,
            0, 0, 0x29,
        )
    )

    LCD_DISPLAY_ON = bytes(
        (
            0, 0, 0x28,
            2, 0, 120,
            0, 0, 0x10,
        )
    )

    LCD_WIDTH = 240
    # LCD_HEIGHT = 280
    LCD_HEIGHT = 320
    LCD_CLK = 26000
    DATA_LINE = 1
    LINE_NUM = 4
    LCD_TYPE = 0
    LCD_SET_BRIGHTNESS = None

    CONTROL_PIN_NUMBER = 20
    TE_PIN_NUMBER = 37
