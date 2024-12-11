import sys_bus
import lvgl as lv
from ..font import Font
from ..language import tr


class SummaryView(lv.canvas):
    SPO2_ICON_SRC = 'E:/media/spo2/bo_dy_icon_{:02d}.png'
    SPO2_NUMBER_SRC = 'E:/media/common/data_hr_32x45.png'
    SPO2_NUMBER_UNIT_SRC = 'E:/media/spo2/bo_data_icon2.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'
    SPO2_HIGHEST_ICON_SRC = 'E:/media/spo2/hr_highest_icon.png'
    SPO2_LOWEST_ICON_SRC = 'E:/media/spo2/hr_lowest_icon.png'
    DIGIT_IMG_SRC = 'E:/media/common/time_small_11x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spo2_label = lv.label(self)
        self.spo2_label.set_size(100, 25)
        self.spo2_label.set_pos(26, 21)
        self.spo2_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.spo2_label.set_text(tr('SpO2'))

        self.time_label = lv.label(self)
        self.time_label.set_size(53, 16)
        self.time_label.set_pos(177, 21)
        self.time_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 36)
        self.side_bar_bg.set_pos(232, 122)

        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 2)

        # self.spo2_icon = lv.animimg(self)
        # anim_imgs = []
        # for i in range(1, 7):
        #     with open(self.SPO2_ICON_SRC.format(i), 'rb') as f:
        #         data = f.read()
        #         anim_imgs.append(
        #             lv.img_dsc_t(
        #                 {
        #                     'data_size': len(data),
        #                     'data': data
        #                 }
        #             )
        #         )
        # self.spo2_icon.set_src(anim_imgs, len(anim_imgs))
        # self.spo2_icon.set_duration(1000)
        # self.spo2_icon.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
        self.spo2_icon = lv.img(self)
        self.spo2_icon.set_src(self.SPO2_ICON_SRC.format(1))
        self.spo2_icon.set_size(97, 121)
        self.spo2_icon.set_pos(77, 35)
        # self.spo2_icon.start()

        self.remaining = lv.label(self)
        self.remaining.set_size(11 * 3, 16)
        self.remaining.set_pos(77 + 97 // 2 - 10, 121 + 40)
        self.remaining.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.remaining.set_text('{}s'.format(30))

        self.spo2_number_high = lv.img(self)
        self.spo2_number_high.set_src(self.SPO2_NUMBER_SRC)
        self.spo2_number_high.set_size(32, 45)
        self.spo2_number_high.set_pos(78, 185)
        self.spo2_number_high.set_offset_y(-45 * 10)

        self.spo2_number_low = lv.img(self)
        self.spo2_number_low.set_src(self.SPO2_NUMBER_SRC)
        self.spo2_number_low.set_size(32, 45)
        self.spo2_number_low.set_pos(110, 185)
        self.spo2_number_low.set_offset_y(-45 * 10)

        self.spo2_number_unit = lv.img(self)
        self.spo2_number_unit.set_src(self.SPO2_NUMBER_UNIT_SRC)
        self.spo2_number_unit.set_size(49, 45)
        self.spo2_number_unit.set_pos(142, 185)

        self.spo2_highest_icon = lv.img(self)
        self.spo2_highest_icon.set_src(self.SPO2_HIGHEST_ICON_SRC)
        self.spo2_highest_icon.set_size(20, 18)
        self.spo2_highest_icon.set_pos(28, 245)

        self.spo2_highest = lv.label(self)
        self.spo2_highest.set_size(22, 16)
        self.spo2_highest.set_pos(28 + 20 + 3, 245 - 2)
        self.spo2_highest.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.spo2_highest.set_text('00')

        self.spo2_lowest_icon = lv.img(self)
        self.spo2_lowest_icon.set_src(self.SPO2_LOWEST_ICON_SRC)
        self.spo2_lowest_icon.set_size(20, 18)
        self.spo2_lowest_icon.set_pos(165, 245)

        self.spo2_lowest = lv.label(self)
        self.spo2_lowest.set_size(22, 16)
        self.spo2_lowest.set_pos(165 + 20 + 3, 245 - 2)
        self.spo2_lowest.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.spo2_lowest.set_text('00')

        self.text = lv.label(self)
        self.text.set_size(130, 24)
        self.text.set_pos(55, 246)
        self.text.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.text.set_text(tr('Checking'))
        self.text.add_style(Font.get('lv_font_24'), lv.PART.MAIN)

        self.reset()

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))

    def update_spo2(self, value):
        value_string = '{:02d}'.format(value)
        self.spo2_number_high.set_offset_y(-45 * int(value_string[0]))
        self.spo2_number_low.set_offset_y(-45 * int(value_string[1]))
        self.spo2_number_unit.clear_flag(lv.obj.FLAG.HIDDEN)

    def update_spo2_highest_and_lowest(self, highest_value, lowest_value):
        self.spo2_highest.set_text('{:02d}'.format(highest_value))
        self.spo2_lowest.set_text('{:02d}'.format(lowest_value))
        self.spo2_highest.clear_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_highest_icon.clear_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_lowest.clear_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_lowest_icon.clear_flag(lv.obj.FLAG.HIDDEN)
        self.text.add_flag(lv.obj.FLAG.HIDDEN)

    def update_spo2_remaining(self, value, hidden=False):
        if hidden:
            self.remaining.add_flag(lv.obj.FLAG.HIDDEN)
            return
        self.remaining.clear_flag(lv.obj.FLAG.HIDDEN)
        self.remaining.set_text('{:02d}s'.format(value))

    def reset(self):
        self.remaining.add_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_number_unit.add_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_number_high.set_offset_y(-45 * 10)
        self.spo2_number_low.set_offset_y(-45 * 10)
        self.spo2_highest.add_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_highest_icon.add_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_lowest.add_flag(lv.obj.FLAG.HIDDEN)
        self.spo2_lowest_icon.add_flag(lv.obj.FLAG.HIDDEN)
        self.text.clear_flag(lv.obj.FLAG.HIDDEN)


class SpO2ChartView(lv.img):
    BO_BG_02_SRC = 'E:/media/spo2/bo_bg_02.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_src(self.BO_BG_02_SRC)
        self.set_size(222, 123)
        self.set_pos(5, 140)

        self.columns = []
        for i in range(24):
            obj = lv.obj(self)
            obj.set_size(4, 0)
            obj.set_pos(31 + (i * 8), 6)
            obj.set_style_radius(20, lv.PART.MAIN)
            obj.set_style_border_width(0, lv.PART.MAIN)
            obj.set_style_bg_color(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN)
            self.columns.append(obj)

    def update(self, hour, lowest, highest):
        self.columns[hour].set_pos(31 + hour * 8, 6 + (100 - highest) * 5)
        self.columns[hour].set_height((highest - lowest) * 5)


class DetailView(lv.canvas):
    BO_BG_01_SRC = 'E:/media/spo2/bo_bg_01.png'
    DIGIT_IMG_SRC = 'E:/media/common/activity_data_18x25.png'
    UNIT_IMG_SRC = 'E:/media/spo2/bo_data_icon3.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spo2_label = lv.label(self)
        self.spo2_label.set_size(100, 25)
        self.spo2_label.set_pos(26, 21)
        self.spo2_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.spo2_label.set_text(tr('SpO2'))

        self.time_label = lv.label(self)
        self.time_label.set_size(53, 16)
        self.time_label.set_pos(177, 21)
        self.time_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 36)
        self.side_bar_bg.set_pos(232, 122)

        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 18)

        self.bo_bg1 = lv.img(self)
        self.bo_bg1.set_src(self.BO_BG_01_SRC)
        self.bo_bg1.set_size(224, 80)
        self.bo_bg1.set_pos(8, 55)

        self.title1 = lv.label(self.bo_bg1)
        self.title1.set_size(204, 24)
        self.title1.set_pos(10, 7)
        self.title1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.title1.set_text(tr('Normal SpO2'))

        self.title2 = lv.label(self.bo_bg1)
        self.title2.set_size(204, 24)
        self.title2.set_pos(10, 7)
        self.title2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.title2.set_text(tr('Normal SpO2'))

        self.num1 = lv.img(self.bo_bg1)
        self.num1.set_src(self.DIGIT_IMG_SRC)
        self.num1.set_size(18, 25)
        self.num1.set_pos(11, 44)
        self.num1.set_offset_y(-25 * 9)

        self.num2 = lv.img(self.bo_bg1)
        self.num2.set_src(self.DIGIT_IMG_SRC)
        self.num2.set_size(18, 25)
        self.num2.set_pos(30, 44)
        self.num2.set_offset_y(-25 * 5)

        self.unit1 = lv.img(self.bo_bg1)
        self.unit1.set_src(self.UNIT_IMG_SRC)
        self.unit1.set_size(29, 25)
        self.unit1.set_pos(49, 44)

        self.separator = lv.img(self.bo_bg1)
        self.separator.set_src(self.DIGIT_IMG_SRC)
        self.separator.set_size(29, 25)
        self.separator.set_pos(78, 44)
        self.separator.set_offset_y(-25 * 10)

        self.num3 = lv.img(self.bo_bg1)
        self.num3.set_src(self.DIGIT_IMG_SRC)
        self.num3.set_size(18, 25)
        self.num3.set_pos(97, 44)
        self.num3.set_offset_y(-25 * 1)

        self.num4 = lv.img(self.bo_bg1)
        self.num4.set_src(self.DIGIT_IMG_SRC)
        self.num4.set_size(18, 25)
        self.num4.set_pos(116, 44)
        self.num4.set_offset_y(0)

        self.num5 = lv.img(self.bo_bg1)
        self.num5.set_src(self.DIGIT_IMG_SRC)
        self.num5.set_size(18, 25)
        self.num5.set_pos(135, 44)
        self.num5.set_offset_y(0)

        self.unit2 = lv.img(self.bo_bg1)
        self.unit2.set_src(self.UNIT_IMG_SRC)
        self.unit2.set_size(29, 25)
        self.unit2.set_pos(154, 44)

        self.chart = SpO2ChartView(self)

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))


class SpO2View(lv.tabview):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, lv.DIR.RIGHT, 0, *args, **kwargs)
        self.set_size(240, 320)
        self.set_pos(0, 0)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        self.tab0 = self.add_tab("tab0")
        self.tab0.set_style_pad_all(0, lv.PART.MAIN)
        self.summary = SummaryView(self.tab0)

        self.tab1 = self.add_tab("tab1")
        self.tab1.set_style_pad_all(0, lv.PART.MAIN)
        self.detail = DetailView(self.tab1)

        self.summary.update_spo2(97)
        self.summary.update_spo2_highest_and_lowest(100, 55)
        for hour in range(24):
            self.detail.chart.update(hour, 90, 97)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_time(self, now):
        self.summary.update_time(now.hour, now.minute, now.second)
        self.detail.update_time(now.hour, now.minute, now.second)

    def update_spo2(self, value):
        self.summary.update_spo2(value)

    def update_spo2_highest_and_lowest(self, data):
        self.summary.update_spo2_highest_and_lowest(data['highest_value'], data['lowest_value'])

    def update_spo2_remaining(self, data):
        self.summary.update_spo2_remaining(data['value'], hidden=data['hidden'])

    def update_spo2_chart(self, data):
        self.detail.chart.update(data['hour'], data['lowest'], data['highest'])
