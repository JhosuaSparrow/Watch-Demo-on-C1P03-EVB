import lvgl as lv
from machine import LCD, Pin, SPI
from misc import Power
from tp import cst816


init_data = (

    0, 0, 0x11,
    2, 0, 120,

    0, 1, 0x36,
    1, 1, 0x00,

    0, 1, 0x3A,
    1, 1, 0x05,  # 05 RGB565;06 RGB666

    0, 5, 0xB2,
    1, 1, 0x0C,
    1, 1, 0x0C,
    1, 1, 0x00,
    1, 1, 0x33,
    1, 1, 0x33,

    0, 1, 0xB7,
    1, 1, 0x56,

    0, 1, 0xBB,
    1, 1, 0x20,

    0, 1, 0xC0,
    1, 1, 0x2C,

    0, 1, 0xC2,
    1, 1, 0x01,

    0, 1, 0xC3,
    1, 1, 0x0F,

    0, 1, 0xC4,
    1, 1, 0x20,

    0, 1, 0xC6,
    1, 1, 0x0F,

    0, 2, 0xD0,
    1, 1, 0xA4,
    1, 1, 0xA1,

    0, 1, 0xD6,
    1, 1, 0xA1,

    0, 14, 0xE0,
    1, 1, 0xF0,
    1, 1, 0x00,
    1, 1, 0x06,
    1, 1, 0x06,
    1, 1, 0x07,
    1, 1, 0x05,
    1, 1, 0x30,
    1, 1, 0x44,
    1, 1, 0x48,
    1, 1, 0x38,
    1, 1, 0x11,
    1, 1, 0x10,
    1, 1, 0x2E,
    1, 1, 0x34,

    0, 14, 0xE1,
    1, 1, 0xF0,
    1, 1, 0x0A,
    1, 1, 0x0E,
    1, 1, 0x0D,
    1, 1, 0x0B,
    1, 1, 0x27,
    1, 1, 0x2F,
    1, 1, 0x44,
    1, 1, 0x47,
    1, 1, 0x35,
    1, 1, 0x12,
    1, 1, 0x12,
    1, 1, 0x2C,
    1, 1, 0x32,

    0, 1, 0x35,
    1, 1, 0x00,

    0, 0, 0x21,

    0, 0, 0x29,
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

init_buf = bytearray(init_data)

init_data2 = (
    0, 4, 0x2a,
    1, 1, XSTART_H,
    1, 1, XSTART_L,
    1, 1, XEND_H,
    1, 1, XEND_L,
    0, 4, 0x2b,
    1, 1, YSTART_H,
    1, 1, YSTART_L,
    1, 1, YEND_H,
    1, 1, YEND_L,
    0, 0, 0x2c,
)
invalid = bytearray(init_data2)

init_data3 = (
    0, 0, 0x28,
    2, 0, 120,
    0, 0, 0x10,
)
displayoff = bytearray(init_data3)

init_data4 = (
    0, 0, 0x11,
    2, 0, 20,
    0, 0, 0x29,
)
displayon = bytearray(init_data4)

Power.camVDD2V8Enable(1)
# lcd.lcd_init(init_buf, 240, 240, 26000, 1, 4, 0, invalid, displayon, displayoff, None)
lcd.lcd_init(init_buf, 240, 320, 52000, 1, 4, 0, invalid, displayon, displayoff, None)

# screen_jud = lcd.readID(0x04)
# # screen_jud = 11
# print("lcd.readID:", screen_jud)

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
disp_drv.register()

# # CST816初始化
# # tp_cst816 = cst816(i2c_no=0,irq=12,reset=16)
# tp_cst820 = cst816(i2c_no=0, irq=12, reset=16, addr=0x15, x_reverse=1, y_reverse=0)
# tp_cst820.activate()
# # LVGL触摸注册
# indev_drv = lv.indev_drv_t()
# indev_drv.init()
# indev_drv.type = lv.INDEV_TYPE.POINTER
# indev_drv.read_cb = tp_cst820.read
# indev_drv.long_press_time = 80
# indev_drv.register()
# tp_gpio = Pin(Pin.GPIO12, Pin.OUT, Pin.PULL_PU, 0)
#
# lcd_bl_gpio = Pin(Pin.GPIO44, Pin.OUT, Pin.PULL_DISABLE, 1)
# # 启动lvgv线程
# lv.tick_inc(5)
# lv.task_handler()
#
# import utime
#
# # 开机画面
# style_font_youyuan_40 = lv.style_t()
# style_font_youyuan_40.init()
# style_font_youyuan_40.set_text_color(lv.color_make(0xff, 0xff, 0xff))
#
# style_screen = lv.style_t()
# style_screen.init()
# style_screen.set_radius(0)
# style_screen.set_bg_color(lv.color_make(0x00, 0x00, 0x00))
# style_screen.set_bg_opa(255)
# style_screen.set_border_width(0)
# style_screen.set_pad_left(0)
# style_screen.set_pad_right(0)
# style_screen.set_pad_top(0)
# style_screen.set_pad_bottom(0)
# # scrollbar组件
# style_list_scrollbar = lv.style_t()
# style_list_scrollbar.init()
# style_list_scrollbar.set_radius(3)
# style_list_scrollbar.set_bg_color(lv.color_hex(0xffffff))
# style_list_scrollbar.set_bg_grad_color(lv.color_hex(0xffffff))
# style_list_scrollbar.set_bg_grad_dir(lv.GRAD_DIR.VER)
# style_list_scrollbar.set_bg_opa(0)
#
#
# # tileview组件
# tileview_screen = lv.obj()
# tileview = lv.tileview(tileview_screen)
#
#
# # 事件处理函数
# def event_handler(e):
#     code = e.get_code()
#     if code == lv.EVENT.VALUE_CHANGED:
#         current_tile = e.get_target().get_tile_act()
#         # 这里的系数
#         print("current tile {}".format(current_tile.get_x() / 240))
#
#
# # 为 tileview 添加事件处理
# tileview.add_event_cb(event_handler, lv.EVENT.VALUE_CHANGED, None)
# # # 设置 tileview 的有效滑动方向
# tileview.set_scroll_dir(lv.DIR.HOR)
#
# # 界面1, 放在x轴0的位置
# tile1 = tileview.add_tile(0, 0, lv.DIR.RIGHT)
# hello_screen = lv.obj(tile1)
# hello_screen.set_size(240, 320)
# # hello_screen.add_style(style_list_scrollbar, lv.PART.MAIN | lv.STATE.DEFAULT)
# # hello_screen.add_style(style_list_scrollbar, lv.PART.SCROLLBAR | lv.STATE.SCROLLED)
# hello_screen.add_style(style_screen, lv.PART.MAIN | lv.STATE.DEFAULT)
# hello_label = lv.label(hello_screen)
# hello_label.set_text("hello")
# hello_label.align(lv.ALIGN.CENTER, 0, 0)
# hello_label.add_style(style_font_youyuan_40, lv.PART.MAIN | lv.STATE.DEFAULT)
# lv.scr_load(tileview_screen)
#
# # 界面2
# # 界面1, 放在x轴1的位置
# tile2 = tileview.add_tile(1, 0, lv.DIR.RIGHT | lv.DIR.LEFT)
# world_screen = lv.obj(tile2)
# world_screen.set_size(240, 320)
# world_screen.add_style(style_list_scrollbar, lv.PART.MAIN | lv.STATE.DEFAULT)
# world_screen.add_style(style_list_scrollbar, lv.PART.SCROLLBAR | lv.STATE.SCROLLED)
# world_screen.add_style(style_screen, lv.PART.MAIN | lv.STATE.DEFAULT)
# world_label = lv.label(world_screen)
# world_label.set_text("world")
# world_label.align(lv.ALIGN.CENTER, 0, 0)
# world_label.add_style(style_font_youyuan_40, lv.PART.MAIN | lv.STATE.DEFAULT)
# #
# # 界面3
# # 界面1, 放在x轴2的位置
# tile3 = tileview.add_tile(2, 0, lv.DIR.LEFT)
# main_screen = lv.obj(tile3)
# main_screen.set_size(240, 320)
# main_screen.add_style(style_list_scrollbar, lv.PART.MAIN | lv.STATE.DEFAULT)
# main_screen.add_style(style_list_scrollbar, lv.PART.SCROLLBAR | lv.STATE.SCROLLED)
# main_screen.add_style(style_screen, lv.PART.MAIN | lv.STATE.DEFAULT)
# main_label = lv.label(main_screen)
# main_label.set_text("QuecPython")
# main_label.align(lv.ALIGN.CENTER, 0, 0)
# main_label.add_style(style_font_youyuan_40, lv.PART.MAIN | lv.STATE.DEFAULT)
