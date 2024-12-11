import lvgl as lv
from tp import cst816 as Cst816
from machine import Pin, LCD, ExtInt
from usr.qframe.threading import Thread
from .config import LcdConfig
from .main_view import *
from .menu_list_view import *
from .telephone_view import *
from .alarm_view import *
from usr.topics import LOAD_MAIN_VIEW, LOAD_MENU_LIST_VIEW


class BaseGUIService(object):
    """lcd、lvgl、tp初始化"""

    def __init__(self, app=None):
        self.lcd = None
        self.lv = None
        self.tp_cst816 = None
        self.indev_drv = None
        self.disp_drv = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register('gui', self)

    def load(self):
        self.init_lcd()
        self.init_tp()
        self.init_lv()

    def init_lcd(self):
        self.lcd = LCD()
        self.lcd.lcd_init(
            LcdConfig.LCD_INIT_DATA,
            LcdConfig.LCD_WIDTH,
            LcdConfig.LCD_HEIGHT,
            LcdConfig.LCD_CLK,
            LcdConfig.DATA_LINE,
            LcdConfig.LINE_NUM,
            LcdConfig.LCD_TYPE,
            LcdConfig.LCD_INVALID,
            LcdConfig.LCD_DISPLAY_ON,
            LcdConfig.LCD_DISPLAY_OFF,
            LcdConfig.LCD_SET_BRIGHTNESS,
        )

    def init_lv(self):
        lv.init()

        # init display driver
        disp_buf1 = lv.disp_draw_buf_t()
        buf_length = LcdConfig.LCD_WIDTH * LcdConfig.LCD_HEIGHT * 2
        disp_buf1.init(bytearray(buf_length), None, buf_length)
        # disp_buf1.init(bytearray(buf_length), bytearray(buf_length), buf_length)  # 双buffer缓冲，占用过多RAM

        self.disp_drv = lv.disp_drv_t()
        self.disp_drv.init()
        self.disp_drv.draw_buf = disp_buf1
        self.disp_drv.flush_cb = self.lcd.lcd_write
        self.disp_drv.hor_res = LcdConfig.LCD_WIDTH
        self.disp_drv.ver_res = LcdConfig.LCD_HEIGHT
        # self.disp_drv.sw_rotate = 1  # 此处设置是否需要旋转
        # self.disp_drv.rotated = lv.DISP_ROT._270  # 旋转角度
        self.disp_drv.register()

        # init input driver
        self.indev_drv = lv.indev_drv_t()
        self.indev_drv.init()
        self.indev_drv.type = lv.INDEV_TYPE.POINTER
        self.indev_drv.read_cb = self.tp_cst816.read
        self.indev_drv.long_press_time = 400  # 400，表示长按的时间阈值，即按住一个点的时间超过该值时，触发长按事件。
        self.indev_drv.scroll_limit = 10  # 10，表示在拖动对象之前，需要滑动的像素数。
        self.indev_drv.scroll_throw = 10  # 10，表示滚动减速的百分比，值越大则减速越快。
        self.indev_drv.gesture_limit = 10  # 50，表示手势滑动的阈值，即只有滑动偏移累计（绝对值）超过这个值才会触发手势动作。
        self.indev_drv.gesture_min_velocity = 3  # 3，表示判断手势触发的最小差值。
        self.indev_drv.register()
        Pin(44, Pin.OUT, Pin.PULL_DISABLE, 0)

        # image cache
        lv.img.cache_invalidate_src(None)
        lv.img.cache_set_size(50)

        # start lvgl thread
        lv.tick_inc(5)
        lv.task_handler()

    def init_tp(self):
        # Pin(44, Pin.OUT, Pin.PULL_DISABLE, 1)
        Pin(31, Pin.OUT, Pin.PULL_DISABLE, 1)
        self.tp_cst816 = Cst816(i2c_no=0, irq=44, reset=31, addr=0x15)
        self.tp_cst816.init()
        # self.tp_cst816.set_callback(self.ui_callback)
        self.tp_cst816.activate()

    @staticmethod
    def ui_callback(para):
        if para == 0:
            print("tp: <-")
        elif para == 1:
            print("tp: ->")
        elif para == 2:
            print("tp: ^")
        elif para == 3:
            print("tp: V")
        elif para == 4:
            print("tp: return")
        elif para == 5:
            print("tp: CLICK")
        elif para == 6:
            print("tp: error")


class GUIService(BaseGUIService):
    """UI切换逻辑"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home_btn = ExtInt(
            ExtInt.GPIO28, ExtInt.IRQ_FALLING,
            ExtInt.PULL_PU,
            lambda _: Thread(target=self.home_btn_click_cb).start()
        )
        self.ctrl_pin = Pin(
            getattr(Pin, 'GPIO{}'.format(LcdConfig.CONTROL_PIN_NUMBER)),
            Pin.OUT,
            Pin.PULL_DISABLE,
            0
        )

    def load(self):
        super().load()
        self.home_btn_click_cb()  # create main view (tileview) first
        self.home_btn.enable()
        self.ctrl_pin.write(1)

    @staticmethod
    def home_btn_click_cb():
        mv = MainView()
        if lv.scr_act() == mv:
            if mv.get_view_name_by_tile_id(mv.get_tile_act().get_child_id()) == 'primary_view':
                sys_bus.publish(LOAD_MENU_LIST_VIEW, {})
            else:
                mv.goto_primary()
        else:
            sys_bus.publish(LOAD_MAIN_VIEW, {'view_name': 'primary_view'})


gui_service = GUIService()
