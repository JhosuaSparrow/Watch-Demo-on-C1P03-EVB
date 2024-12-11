import utime
import _thread
from machine import Pin
from misc import Power

gpio1 = Pin(Pin.GPIO20, Pin.OUT, Pin.PULL_DISABLE, 1)
gpio2 = Pin(Pin.GPIO37, Pin.OUT, Pin.PULL_DISABLE, 1)
gpio3 = Pin(Pin.GPIO44, Pin.OUT, Pin.PULL_DISABLE, 1)
Power.camVDD2V8Enable(1)

test = (
    2, 0, 120,
    0, 0, 0x11,
    0, 1, 0x36,
    1, 1, 0x00,
    # 0, 1, 0x36,
    # 1, 1, 0x00,
    0, 1, 0x3A,
    1, 1, 0x05,
    0, 0, 0x21,
    0, 5, 0xB2,
    1, 1, 0x05,
    1, 1, 0x05,
    1, 1, 0x00,
    1, 1, 0x33,
    1, 1, 0x33,
    0, 1, 0xB7,
    1, 1, 0x23,
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
    1, 1, 0x0F,
    0, 2, 0xD0,
    1, 1, 0xA4,
    1, 1, 0xA1,
    0, 1, 0xD6,
    1, 1, 0xA1,
    0, 14, 0xE0,
    1, 1, 0x70,
    1, 1, 0x06,
    1, 1, 0x0C,
    1, 1, 0x08,
    1, 1, 0x09,
    1, 1, 0x27,
    1, 1, 0x2E,
    1, 1, 0x34,
    1, 1, 0x46,
    1, 1, 0x37,
    1, 1, 0x13,
    1, 1, 0x13,
    1, 1, 0x25,
    1, 1, 0x2A,
    0, 14, 0xE1,
    1, 1, 0x70,
    1, 1, 0x04,
    1, 1, 0x08,
    1, 1, 0x09,
    1, 1, 0x07,
    1, 1, 0x03,
    1, 1, 0x2C,
    1, 1, 0x42,
    1, 1, 0x42,
    1, 1, 0x38,
    1, 1, 0x14,
    1, 1, 0x14,
    1, 1, 0x27,
    1, 1, 0x2C,
    0, 0, 0x29,
    0, 4, 0x2a,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0xef,
    0, 4, 0x2b,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0x01,
    1, 1, 0x3f,
    0, 0, 0x2c,

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

from machine import LCD
import utime

lcd = LCD()

test1 = bytearray(test)

test2 = (
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
test_invalid = bytearray(test2)

test3 = (
    0, 0, 0x28,
    2, 0, 120,
    0, 0, 0x10,
)
test_displayoff = bytearray(test3)

test4 = (
    0, 0, 0x11,
    2, 0, 20,
    0, 0, 0x29,
)
test_displayon = bytearray(test4)


lcd.lcd_init(test1, 240, 320, 52000, 1, 4, 0, test_invalid, test_displayon, test_displayoff, None)
# lcd.lcd_init(test1, 240, 320, 52000, 1, 4, 0, test_invalid, test_displayon, test_displayoff, None, TESel=True, TEPin=Pin.GPIO37)
# lcd.lcd_init(test1, 240,320,4,1,4,0,test_invalid,test_displayon,test_displayoff,None,1, 0, 0, 2, 4, 31)
# res = lcd.readID(0x3a)
# print(res)
utime.sleep(2)
lcd.lcd_clear(0xF800)
lcd.lcd_brightness(5)
lcd.lcd_display_on()


# -----------------------------------------

import lvgl as lv
lv.init()
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytes(240*320*2)
disp_buf1.init(buf1_1, None, len(buf1_1))
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = lcd.lcd_write
disp_drv.hor_res = 240              #此处基于实际的屏幕来设置水平分辨率
disp_drv.ver_res = 320              #此处基于实际的屏幕来设置垂直分辨率
disp_drv.register()
lv.tick_inc(5)
lv.task_handler()

s = lv.obj()
test = lv.img(s)
lv.scr_load(s)


test.set_src('img:bg1.jpg')
utime.sleep(3)
test.set_src('img:bg2.jpg')


# screens = []
# for num in range(1, 6):
#     s = lv.obj()
#     screens.append(s)
#     img1 = lv.img(s)
#     img1.set_src("U:/{}.jpg".format(num))
#
#
# def test_show():
#     index = 0
#     while True:
#         lv.scr_load(screens[index])
#         index = (index + 1) % 5
#
#
# _thread.start_new_thread(test_show, ())


# import camera
# bb = camera.camScandecode(0,1,640,480,1,240,240)
# bb.open()
# bb.callback(fun)
# bb.start()

# def fun(para):
# print(para)

# import camera
# preview1 = camera.camPreview(0,640,480,240,240,1)
# preview1.open()


# # import camera
# # aa = camera.camCaputre(0,640,480,240,240,1)
# # aa.open()
# # aa.start(240,240,'11')


# # # import camera
# # # scan = camera.camScandecode(1,1,640,480,1,240,240)
# # # scan.open()
# # # scan.start()
# import camera
# preview1 = camera.camPreview(1,640,480,240,240,1)
# preview1.open()
# preview1.close()
# preview1.open()

# # # import camera
# # # scan = camera.camScandecode(1,1,640,480,1,240,240)
# # # scan.open()
# # # scan.start()

# # # utime.sleep(2)

# # def lcd_fun(arg1,arg2,arg3):
# # print("hhhhhh")


# # print('lvgl start1')
# # import lvgl as lv
# # lv.init()
# # disp_buf1 = lv.disp_buf_t()
# # buf1_1 = bytes(240*240*2)
# # disp_buf1.init(buf1_1, None, len(buf1_1))
# # disp_drv = lv.disp_drv_t()
# # disp_drv.init()
# # disp_drv.buffer = disp_buf1
# # disp_drv.flush_cb = lcd.lcd_write
# # disp_drv.hor_res = 240
# # disp_drv.ver_res = 240
# # disp_drv.register()

# # lv.tick_inc(5)
# # lv.task_handler()

# # print('lvgl start1')
# # import lvgl as lv
# # lv.init()
# # disp_buf1 = lv.disp_buf_t()
# # buf1_1 = bytes(240*240*2)
# # lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1))
# # disp_drv = lv.disp_drv_t()
# # lv.disp_drv_init(disp_drv)
# # disp_drv.buffer = disp_buf1
# # disp_drv.flush_cb = lcd.lcd_write
# # disp_drv.hor_res = 240
# # disp_drv.ver_res = 240
# # lv.disp_drv_register(disp_drv)

# # lv.tick_inc(5)
# # lv.task_handler()

# # g_poc_style_plain_11 = lv.style_t(lv.style_plain)
# # g_poc_style_plain_11.body.main_color = lv.color_hex(0xf800)
# # g_poc_style_plain_11.body.grad_color = lv.color_hex(0x001f)
# # g_poc_style_plain_11.text.color = lv.color_hex(0xffffff)
# # g_poc_style_plain_11.text.font = lv.font_chinese_9

# # act_group = lv.group_create()
# # father = lv.obj()
# # obj2 = lv.obj(father)
# # lv.obj.set_hidden(obj2,False)
# # obj2.set_style(g_poc_style_plain_11)
# # obj2.set_pos(0,0)
# # obj2.set_size(240,240)
# # lv.scr_load(father)

# # #lv.theme_set_current(lv.theme_night_init(0, lv.font_roboto_16))

# # status_label_time=lv.label(obj2)
# # status_label_time.set_text("10:01")
# # status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # status_label_time.align(None, lv.ALIGN.IN_TOP_LEFT,0,2)


# # g_poc_style_plain_symbol = lv.style_t(lv.style_plain)
# # g_poc_style_plain_symbol.body.main_color = lv.color_hex(0xf800)
# # g_poc_style_plain_symbol.body.grad_color = lv.color_hex(0x001f)
# # g_poc_style_plain_symbol.text.color = lv.color_hex(0xffffff)
# # g_poc_style_plain_symbol.text.font = lv.font_chinese_9

# # status_label_symbol_nw_mode=lv.label(obj2)
# # status_label_symbol_nw_mode.set_text("0G")
# # status_label_symbol_nw_mode.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # status_label_symbol_nw_mode.align(status_label_time, lv.ALIGN.OUT_RIGHT_TOP,55,0)


# # status_label_symbol_csq=lv.label(obj2)
# # status_label_symbol_csq.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_symbol)
# # status_label_symbol_csq.set_text("\xef\x80\x92")
# # status_label_symbol_csq.align(status_label_symbol_nw_mode, lv.ALIGN.OUT_RIGHT_TOP,3,0)
# # status_label_symbol_csq.set_y(0)

# # status_label_symbol_battery=lv.label(obj2)
# # status_label_symbol_battery.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_symbol)
# # status_label_symbol_battery.set_text("\xef\x89\x81")
# # status_label_symbol_battery.align(status_label_symbol_csq, lv.ALIGN.OUT_RIGHT_TOP,3,0)
# # status_label_symbol_battery.set_y(0)


# # obj1 = lv.obj(father)
# # obj1.set_style(g_poc_style_plain_11)
# # obj1.set_pos(0,61)
# # obj1.set_size(240,49)

# # g_information_screen = lv.obj(obj1)
# # g_information_screen.set_style(g_poc_style_plain_11)
# # g_information_screen.set_pos(0,0)
# # g_information_screen.set_size(240,19)

# # menu_info_label = lv.label(g_information_screen)
# # menu_info_label.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # menu_info_label.set_text("this is lvgl test quectel shits s ffadfsd@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# # menu_info_label.set_long_mode(4)
# # menu_info_label.set_pos(2,1)
# # menu_info_label.set_size(128,50)

# # list_lcal_infomation = lv.list(g_information_screen)
# # list_lcal_infomation.set_style(lv.list.STYLE.BG,g_poc_style_plain_11)
# # list_lcal_infomation.set_pos(0,20)
# # list_lcal_infomation.set_size(128,30)
# # lv.scr_load(father)
# # print('lvgl end')

# # # print('lvgl start1')
# # # import lvgl as lv
# # # lv.init()
# # # disp_buf1 = lv.disp_buf_t()
# # # buf1_1 = bytes(240*240*2)
# # # lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1))
# # # disp_drv = lv.disp_drv_t()
# # # lv.disp_drv_init(disp_drv)
# # # disp_drv.buffer = disp_buf1
# # # disp_drv.flush_cb = lcd.lcd_write
# # # disp_drv.hor_res = 240
# # # disp_drv.ver_res = 240
# # # lv.disp_drv_register(disp_drv)

# # # lv.tick_inc(5)
# # # lv.task_handler()

# # # g_poc_style_plain_11 = lv.style_t(lv.style_plain)
# # # g_poc_style_plain_11.body.main_color = lv.color_hex(0xf800)
# # # g_poc_style_plain_11.body.grad_color = lv.color_hex(0x001f)
# # # g_poc_style_plain_11.text.color = lv.color_hex(0x0000)
# # # g_poc_style_plain_11.text.font = lv.font_chinese_11

# # # act_group = lv.group_create()
# # # father = lv.obj()
# # # obj2 = lv.obj(father)
# # # lv.obj.set_hidden(obj2,False)
# # # obj2.set_style(g_poc_style_plain_11)
# # # obj2.set_pos(0,0)
# # # obj2.set_size(240,240)
# # # lv.scr_load(father)
# # # utime.sleep(2)

# # # status_label_time=lv.label(obj2)
# # # status_label_time.set_text("移远出品,必属精品")
# # # status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # # # status_label_time.align(None, lv.ALIGN.IN_TOP_LEFT,0,2)
# # # utime.sleep(2)

# # # index = 0
# # # x_start = 0
# # # y_start = 0
# # # x_end = 240 - status_label_time.get_width()
# # # y_end = 240 - status_label_time.get_height()
# # # while 1:
# # #     g_poc_style_plain_11.body.main_color = lv.color_hex(0xfff0)
# # #     g_poc_style_plain_11.body.grad_color = lv.color_hex(0xfff0)
# # #     status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # #     for num in range(0,20):     
# # #         status_label_time.set_x(x_start)
# # #         status_label_time.set_y(y_start)
# # #         if(num == 0):
# # #             obj2.set_style(g_poc_style_plain_11)
# # #         x_start = x_start + 5
# # #         y_start = y_start + 5 
# # #         utime.sleep_ms(50)
# # #         if(x_start > x_end or y_start == y_end):
# # #             break

# # #     g_poc_style_plain_11.body.main_color = lv.color_hex(0xff0f)
# # #     g_poc_style_plain_11.body.grad_color = lv.color_hex(0xff0f)
# # #     obj2.set_style(g_poc_style_plain_11)
# # #     status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # #     for num in range(0, 20):
# # #         status_label_time.set_x(x_start)
# # #         status_label_time.set_y(y_start)
# # #         if(num == 0):
# # #             obj2.set_style(g_poc_style_plain_11)
# # #         x_start = x_start - 5
# # #         y_start = y_start + 5
# # #         utime.sleep_ms(50)
# # #         if(x_start == 0 or y_start == y_end):
# # #             break
# # #     g_poc_style_plain_11.body.main_color = lv.color_hex(0xf0ff)
# # #     g_poc_style_plain_11.body.grad_color = lv.color_hex(0xf0ff)
# # #     obj2.set_style(g_poc_style_plain_11)
# # #     status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # #     for num in range(0, 20):
# # #         status_label_time.set_x(x_start)
# # #         status_label_time.set_y(y_start)
# # #         if(num == 0):
# # #             obj2.set_style(g_poc_style_plain_11)
# # #         x_start = x_start - 5
# # #         y_start = y_start - 5

# # #         utime.sleep_ms(50)
# # #         if(x_start == 0 or y_start == 0):
# # #             break
# # #     g_poc_style_plain_11.body.main_color = lv.color_hex(0x0fff)
# # #     g_poc_style_plain_11.body.grad_color = lv.color_hex(0x0fff)
# # #     obj2.set_style(g_poc_style_plain_11)
# # #     status_label_time.set_style(lv.label.STYLE.MAIN,g_poc_style_plain_11)
# # #     for num in range(0,20):
# # #         status_label_time.set_x(x_start)
# # #         status_label_time.set_y(y_start)
# # #         if(num == 0):
# # #             obj2.set_style(g_poc_style_plain_11)
# # #         x_start = x_start + 5
# # #         y_start = y_start - 5
# # #         utime.sleep_ms(50)
# # #         if(x_start == x_end or y_start == 0):
# # #             break
