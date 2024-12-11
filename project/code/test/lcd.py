import lvgl as lv
from machine import LCD
from machine import ctrl_camera_power

ctrl_camera_power(1)
import utime
utime.sleep(1)


test=(
0, 0, 0x11,
2, 0, 120,

0, 1, 0x36,
1, 1, 0x00,

0, 1, 0x3A,
1, 1, 0x05,

0, 5, 0xB2,
1, 1, 0x0C,
1, 1, 0x0C,
1, 1, 0x00,
1, 1, 0x33,
1, 1, 0x33,

0, 1, 0xB7,
1, 1, 0x56,

0, 1, 0xBB,
1, 1, 0x1D,

0, 1, 0xC0,
1, 1, 0x2C,

0, 1, 0xC2,
1, 1, 0x01,

0, 1, 0xC3,
1, 1, 0x0F,

0, 1, 0xC6,
1, 1, 0x0F,

0, 1, 0xD0,
1, 1, 0xA7,

0, 2, 0xD0,
1, 1, 0xA4,
1, 1, 0xA1,

0, 1, 0xD6,
1, 1, 0xA1,

0, 14, 0xE0,
1, 1, 0xF0,
1, 1, 0x02,
1, 1, 0x07,
1, 1, 0x05,
1, 1, 0x06,
1, 1, 0x14,
1, 1, 0x2F,
1, 1, 0x54,
1, 1, 0x46,
1, 1, 0x38,
1, 1, 0x13,
1, 1, 0x11,
1, 1, 0x24,
1, 1, 0x35,

0, 14, 0xE1,
1, 1, 0xF0,
1, 1, 0x08,
1, 1, 0x0C,
1, 1, 0x0C,
1, 1, 0x09,
1, 1, 0x05,
1, 1, 0x2F,
1, 1, 0x43,
1, 1, 0x46,
1, 1, 0x36,
1, 1, 0x10,
1, 1, 0x12,
1, 1, 0x2C,
1, 1, 0x32,

0, 0, 0x20,
0, 0, 0x29,
2, 0, 120,
0, 0, 0x2C,
)

XSTART_H = 0xf0
XSTART_L = 0xf1
YSTART_H = 0xf2
YSTART_L = 0xf3
XEND_H = 0xE0
XEND_L = 0xE1
YEND_H = 0xE2
YEND_L = 0xE3


XSTART = 0xD0
XEND = 0xD1
YSTART = 0xD2
YEND = 0xD3

lcd = LCD()

test1 = bytearray(test)

test2 = (
0,4,0x2a,
1,1,XSTART_H,
1,1,XSTART_L,
1,1,XEND_H,
1,1,XEND_L,
0,4,0x2b,
1,1,YSTART_H,
1,1,YSTART_L,
1,1,YEND_H,
1,1,YEND_L,
0,0,0x2c,
)
test_invalid = bytearray(test2)

test3 = (
0,0,0x28,
2,0,120,
0,0,0x10,
)
test_displayoff = bytearray(test3)

test4 = (
0,0,0x11,
2,0,120,
0,0,0x29,
)
test_displayon = bytearray(test4)


res1 = lcd.lcd_init(test1, 240,320,14,1,4,0,test_invalid,test_displayon,test_displayoff,None,1,0,0,11,3,45)
print(res1)
lcd.lcd_brightness(5)

LCD_SIZE_W = 240
LCD_SIZE_H = 320
# 初始化lvgl
lv.init()

# Register SDL display driver.
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(LCD_SIZE_W * LCD_SIZE_H * 2)
disp_buf1.init(buf1_1, None, len(buf1_1))
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = lcd.lcd_write
disp_drv.hor_res = LCD_SIZE_W
disp_drv.ver_res = LCD_SIZE_H
# disp_drv.sw_rotate = 1  # 因为横屏，所以需要旋转
# disp_drv.rotated = lv.DISP_ROT._90  # 旋转角度
disp_drv.register()

# 启动lvgv线程
power_on_screen = lv.obj()
power_on_img_screen = lv.img(power_on_screen)
power_on_img_screen.set_size(320, 240)
power_on_img_screen.set_src("U:/logo.jpg")
# power_on_img_screen = JsUtil.dft_img(parent=power_on_screen,size=(SCREEN_WIDTH, SCREEN_HIGH), src="U:/logo.jpg")


lv.tick_inc(5)
lv.scr_load(power_on_screen)
lv.task_handler()
disp_drv.sw_rotate = 1  # 因为横屏，所以需要旋转
disp_drv.rotated = lv.DISP_ROT._90  # 旋转角度
disp_drv.register()

lv.img.cache_invalidate_src(None)
lv.img.cache_set_size(1)