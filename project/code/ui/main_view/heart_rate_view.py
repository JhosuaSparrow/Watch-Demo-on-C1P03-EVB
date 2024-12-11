import sys_bus
import lvgl as lv
from ..language import tr


class SummaryView(lv.canvas):
    HR_ICON_SRC = 'E:/media/heart_rate/hr_dy_icon_{:02d}.png'
    HR_NUMBER_SRC = 'E:/media/common/data_hr_32x45.png'
    HR_NUMBER_UNIT_SRC = 'E:/media/heart_rate/bo_data_icon2.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'
    HR_HIGHEST_ICON_SRC = 'E:/media/heart_rate/hr_highest_icon.png'
    HR_LOWEST_ICON_SRC = 'E:/media/heart_rate/hr_lowest_icon.png'
    DIGIT_IMG_SRC = 'E:/media/common/time_small_11x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hr_label = lv.label(self)
        self.hr_label.set_size(107, 17)
        self.hr_label.set_pos(26, 21)
        self.hr_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.hr_label.set_text(tr('Heart Rate'))

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

        # self.hr_icon = lv.animimg(self)
        # anim_imgs = []
        # for i in range(1, 3):
        #     with open(self.HR_ICON_SRC.format(i), 'rb') as f:
        #         data = f.read()
        #         anim_imgs.append(
        #             lv.img_dsc_t(
        #                 {
        #                     'data_size': len(data),
        #                     'data': data
        #                 }
        #             )
        #         )
        # self.hr_icon.set_src(anim_imgs, len(anim_imgs))
        # self.hr_icon.set_duration(1000)
        # self.hr_icon.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
        self.hr_icon = lv.img(self)
        self.hr_icon.set_src(self.HR_ICON_SRC.format(1))
        self.hr_icon.set_size(80, 68)
        self.hr_icon.set_pos(80, 75)
        # self.hr_icon.start()

        self.hr_number_high = lv.img(self)
        self.hr_number_high.set_src(self.HR_NUMBER_SRC)
        self.hr_number_high.set_size(32, 45)
        self.hr_number_high.set_pos(89, 175)
        self.hr_number_high.set_offset_y(-45 * 10)

        self.hr_number_low = lv.img(self)
        self.hr_number_low.set_src(self.HR_NUMBER_SRC)
        self.hr_number_low.set_size(32, 45)
        self.hr_number_low.set_pos(121, 175)
        self.hr_number_low.set_offset_y(-45 * 10)

        self.hr_number_unit = lv.img(self)
        self.hr_number_unit.set_src(self.HR_NUMBER_UNIT_SRC)
        self.hr_number_unit.set_size(50, 24)
        self.hr_number_unit.set_pos(158, 196)

        self.hr_highest_icon = lv.img(self)
        self.hr_highest_icon.set_src(self.HR_HIGHEST_ICON_SRC)
        self.hr_highest_icon.set_size(20, 18)
        self.hr_highest_icon.set_pos(28, 245)

        self.hr_highest = lv.label(self)
        self.hr_highest.set_size(22, 16)
        self.hr_highest.set_pos(28 + 20 + 3, 245 - 2)
        self.hr_highest.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.hr_highest.set_text('--')

        self.hr_lowest_icon = lv.img(self)
        self.hr_lowest_icon.set_src(self.HR_LOWEST_ICON_SRC)
        self.hr_lowest_icon.set_size(20, 18)
        self.hr_lowest_icon.set_pos(165, 245)

        self.hr_lowest = lv.label(self)
        self.hr_lowest.set_size(22, 16)
        self.hr_lowest.set_pos(165 + 20 + 3, 245 - 2)
        self.hr_lowest.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.hr_lowest.set_text('--')

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))


class HRChartView(lv.img):
    HR_BG_02_SRC = 'E:/media/heart_rate/hr_bg_01.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_src(self.HR_BG_02_SRC)
        self.set_size(227, 185)
        self.set_pos(3, 72)

        self.columns = []
        for i in range(24):
            obj = lv.obj(self)
            obj.set_size(4, 0)
            obj.set_pos(36 + (i * 8), 6)
            obj.set_style_radius(20, lv.PART.MAIN)
            obj.set_style_border_width(0, lv.PART.MAIN)
            obj.set_style_bg_color(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN)
            self.columns.append(obj)

    def update(self, hour, lowest, highest):
        self.columns[hour].set_pos(36 + hour * 8, 6 + int((220 - highest) * 160 / 180))
        self.columns[hour].set_height(int((highest - lowest) * 160 / 180))


class DetailView(lv.canvas):
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hr_label = lv.label(self)
        self.hr_label.set_size(100, 25)
        self.hr_label.set_pos(26, 21)
        self.hr_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.hr_label.set_text(tr('Heart Rate'))

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

        self.chart = HRChartView(self)

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))


class HeartRateView(lv.tabview):

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

        for hour in range(24):
            self.detail.chart.update(hour, 100, 160)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_time(self, now):
        self.summary.update_time(now.hour, now.minute, now.second)
        self.detail.update_time(now.hour, now.minute, now.second)
