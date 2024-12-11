"""功能界面，睡眠数据"""
import sys_bus
import lvgl as lv
from ..language import tr


class SummaryView(lv.canvas):
    SLEEP_ICON_SRC = 'E:/media/sleep/slp_icon_{:02d}.png'
    SLEEP_STAR_ICON_SRC = 'E:/media/sleep/slp_star.png'
    SLEEP_STAR_HIGH_ICON_SRC = 'E:/media/sleep/slp_star_high.png'
    DIGIT_IMG_SRC = 'E:/media/common/data_hr_32x45.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x52.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        self.sleep_label = lv.label(self)
        self.sleep_label.set_size(100, 25)
        self.sleep_label.set_pos(26, 21)
        self.sleep_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.sleep_label.set_text(tr('Sleep'))

        self.time_label = lv.label(self)
        self.time_label.set_size(53, 16)
        self.time_label.set_pos(177, 21)
        self.time_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        # self.sleep_icon = lv.animimg(self)
        # anim_imgs = []
        # for i in range(1, 4):
        #     with open(self.SLEEP_ICON_SRC.format(i), 'rb') as f:
        #         data = f.read()
        #         anim_imgs.append(
        #             lv.img_dsc_t(
        #                 {
        #                   'data_size': len(data),
        #                   'data': data
        #                 }
        #             )
        #         )
        # self.sleep_icon.set_src(anim_imgs, len(anim_imgs))
        # self.sleep_icon.set_duration(1000)
        # self.sleep_icon.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
        self.sleep_icon = lv.img(self)
        self.sleep_icon.set_src(self.SLEEP_ICON_SRC.format(1))
        self.sleep_icon.set_size(56, 56)
        self.sleep_icon.set_pos(92, 57)
        # self.sleep_icon.start()

        self.stars_list = []
        for i in range(5):
            img = lv.img(self)
            img.set_src(self.SLEEP_STAR_ICON_SRC)
            img.set_size(22, 20)
            img.set_pos(55 + 5 + (i * 22), 129)
            self.stars_list.append(img)

        self.slp_hour_high = lv.img(self)
        self.slp_hour_high.set_src(self.DIGIT_IMG_SRC)
        self.slp_hour_high.set_size(32, 45)
        self.slp_hour_high.set_pos(35, 175)

        self.slp_hour_low = lv.img(self)
        self.slp_hour_low.set_src(self.DIGIT_IMG_SRC)
        self.slp_hour_low.set_size(32, 45)
        self.slp_hour_low.set_pos(35 + 35, 175)

        self.slp_hour_unit = lv.label(self)
        self.slp_hour_unit.set_size(15, 18)
        self.slp_hour_unit.set_pos(35 + 35 + 35 + 3, 200)
        self.slp_hour_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_hour_unit.set_text('H')

        self.slp_minute_high = lv.img(self)
        self.slp_minute_high.set_src(self.DIGIT_IMG_SRC)
        self.slp_minute_high.set_size(32, 45)
        self.slp_minute_high.set_pos(35 + 35 + 35 + 20, 175)

        self.slp_minute_low = lv.img(self)
        self.slp_minute_low.set_src(self.DIGIT_IMG_SRC)
        self.slp_minute_low.set_size(32, 45)
        self.slp_minute_low.set_pos(35 + 35 + 35 + 35 + 20, 175)

        self.slp_minute_unit = lv.label(self)
        self.slp_minute_unit.set_size(15, 18)
        self.slp_minute_unit.set_pos(35 + 35 + 35 + 35 + 35 + 20 + 3, 200)
        self.slp_minute_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_minute_unit.set_text('M')

        self.brief = lv.label(self)
        self.brief.set_size(200, 24)
        self.brief.set_pos(47, 239)
        self.brief.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.brief.set_style_text_align(lv.ALIGN.CENTER, lv.PART.MAIN)
        self.brief.set_text(tr('Total Duration'))

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 52)
        self.side_bar_bg.set_pos(232, 114)

        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 2)

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))

    def update_sleep_time(self, hour, minute):
        hour_string = '{:02d}'.format(hour)
        minute_string = '{:02d}'.format(minute)
        self.slp_hour_high.set_offset_y(-45 * int(hour_string[0]))
        self.slp_hour_low.set_offset_y(-45 * int(hour_string[1]))
        self.slp_minute_high.set_offset_y(-45 * int(minute_string[0]))
        self.slp_minute_low.set_offset_y(-45 * int(minute_string[1]))
        sleep_level = (hour * 60 + minute) // 96  # 96 minutes per star, total 8 hours for 5 stars
        for index in range(5):
            self.stars_list[index].set_src(
                self.SLEEP_STAR_HIGH_ICON_SRC if index < sleep_level else self.SLEEP_STAR_ICON_SRC
            )


class DetailView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/common/data_step_22x31.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x52.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'
    SLEEP_DEEP_ICON_SRC = 'E:/media/sleep/slp_deep.png'
    SLEEP_LIGHT_ICON_SRC = 'E:/media/sleep/slp_light.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        self.sleep_label = lv.label(self)
        self.sleep_label.set_size(59, 25)
        self.sleep_label.set_pos(26, 21)
        self.sleep_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.sleep_label.set_text(tr('Sleep'))

        self.time_label = lv.label(self)
        self.time_label.set_size(53, 16)
        self.time_label.set_pos(177, 21)
        self.time_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 52)
        self.side_bar_bg.set_pos(232, 114)

        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 18)

        self.slp_deep_icon = lv.img(self)
        self.slp_deep_icon.set_src(self.SLEEP_DEEP_ICON_SRC)
        self.slp_deep_icon.set_size(10, 31)
        self.slp_deep_icon.set_pos(3, 71)

        self.slp_deep_hour = lv.img(self)
        self.slp_deep_hour.set_src(self.DIGIT_IMG_SRC)
        self.slp_deep_hour.set_size(22, 31)
        self.slp_deep_hour.set_pos(3 + 10 + 10, 71)

        self.slp_deep_hour_unit = lv.label(self)
        self.slp_deep_hour_unit.set_size(15, 18)
        self.slp_deep_hour_unit.set_pos(3 + 10 + 37, 71 + 13)
        self.slp_deep_hour_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_deep_hour_unit.set_text('H')

        self.slp_deep_minute_high = lv.img(self)
        self.slp_deep_minute_high.set_src(self.DIGIT_IMG_SRC)
        self.slp_deep_minute_high.set_size(22, 31)
        self.slp_deep_minute_high.set_pos(3 + 10 + 59, 71)

        self.slp_deep_minute_low = lv.img(self)
        self.slp_deep_minute_low.set_src(self.DIGIT_IMG_SRC)
        self.slp_deep_minute_low.set_size(22, 31)
        self.slp_deep_minute_low.set_pos(3 + 10 + 81, 71)

        self.slp_deep_minute_unit = lv.label(self)
        self.slp_deep_minute_unit.set_size(15, 18)
        self.slp_deep_minute_unit.set_pos(3 + 10 + 108, 71 + 13)
        self.slp_deep_minute_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_deep_minute_unit.set_text('M')

        self.slp_deep_brief = lv.label(self)
        self.slp_deep_brief.set_size(127, 24)
        self.slp_deep_brief.set_pos(3 + 10 + 10, 71 + 31 + 13)
        self.slp_deep_brief.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_deep_brief.set_text(tr('Deep-Sleep'))

        self.slp_light_icon = lv.img(self)
        self.slp_light_icon.set_src(self.SLEEP_LIGHT_ICON_SRC)
        self.slp_light_icon.set_size(10, 31)
        self.slp_light_icon.set_pos(3, 167)

        self.slp_light_hour = lv.img(self)
        self.slp_light_hour.set_src(self.DIGIT_IMG_SRC)
        self.slp_light_hour.set_size(22, 31)
        self.slp_light_hour.set_pos(3 + 10 + 10, 167)

        self.slp_light_hour_unit = lv.label(self)
        self.slp_light_hour_unit.set_size(15, 18)
        self.slp_light_hour_unit.set_pos(3 + 10 + 10 + 22 + 5, 167 + 13)
        self.slp_light_hour_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_light_hour_unit.set_text('H')

        self.slp_light_minute_high = lv.img(self)
        self.slp_light_minute_high.set_src(self.DIGIT_IMG_SRC)
        self.slp_light_minute_high.set_size(22, 31)
        self.slp_light_minute_high.set_pos(3 + 10 + 10 + 22 + 5 + 15 + 7, 167)

        self.slp_light_minute_low = lv.img(self)
        self.slp_light_minute_low.set_src(self.DIGIT_IMG_SRC)
        self.slp_light_minute_low.set_size(22, 31)
        self.slp_light_minute_low.set_pos(3 + 10 + 10 + 22 + 5 + 15 + 7 + 22, 167)

        self.slp_light_minute_unit = lv.label(self)
        self.slp_light_minute_unit.set_size(15, 18)
        self.slp_light_minute_unit.set_pos(3 + 10 + 10 + 22 + 5 + 15 + 7 + 22 + 22 + 5, 167 + 13)
        self.slp_light_minute_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_light_minute_unit.set_text('M')

        self.slp_light_brief = lv.label(self)
        self.slp_light_brief.set_size(127, 24)
        self.slp_light_brief.set_pos(3 + 10 + 10, 167 + 10 + 31)
        self.slp_light_brief.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.slp_light_brief.set_text(tr('Light-Sleep'))

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))

    def update_deep_sleep(self, hour, minute):
        hour_string = '{:02d}'.format(hour)
        minute_string = '{:02d}'.format(minute)
        self.slp_deep_hour.set_offset_y(-31 * int(hour_string[1]))
        self.slp_deep_minute_high.set_offset_y(-31 * int(minute_string[0]))
        self.slp_deep_minute_low.set_offset_y(-31 * int(minute_string[1]))

    def update_light_sleep(self, hour, minute):
        hour_string = '{:02d}'.format(hour)
        minute_string = '{:02d}'.format(minute)
        self.slp_light_hour.set_offset_y(-31 * int(hour_string[1]))
        self.slp_light_minute_high.set_offset_y(-31 * int(minute_string[0]))
        self.slp_light_minute_low.set_offset_y(-31 * int(minute_string[1]))


class SleepChartView(lv.img):
    BG_IMG_SRC = 'E:/media/sleep/slp_bg.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(207, 164)
        self.set_pos(16, 83)
        self.set_src(self.BG_IMG_SRC)

        self.columns = []
        for i in range(7):
            obj = lv.obj(self)
            obj.set_style_radius(0, lv.PART.MAIN)
            obj.set_style_border_width(0, lv.PART.MAIN)
            obj.set_style_bg_color(lv.palette_main(lv.PALETTE.PURPLE), lv.PART.MAIN)
            obj.set_size(8, 0)
            obj.set_pos(31 + (27 * i), 159)
            self.columns.append(obj)

    def update(self, data_list):
        for index, column in enumerate(self.columns):
            height = data_list[index] // 5  # 5 minutes per pix
            column.set_height(height)
            column.set_y(159 - height)


class RecentView(lv.canvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        self.title = lv.label(self)
        self.title.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.title.set_size(204, 25)
        self.title.set_pos(20, 15)
        self.title.set_text(tr('Last 7 days of sleep'))

        self.chart = SleepChartView(self)


class SleepView(lv.tabview):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, lv.DIR.RIGHT, 0, *args, **kwargs)
        self.set_size(240, 320)
        self.set_pos(0, 0)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        # 睡眠数据总览
        self.tab0 = self.add_tab("tab0")
        self.tab0.set_style_pad_all(0, lv.PART.MAIN)
        self.summary = SummaryView(self.tab0)

        # 睡眠数据详情
        self.tab1 = self.add_tab("tab1")
        self.tab1.set_style_pad_all(0, lv.PART.MAIN)
        self.detail = DetailView(self.tab1)

        # 近7天睡眠数据
        self.tab2 = self.add_tab("tab2")
        self.tab2.set_style_pad_all(0, lv.PART.MAIN)
        self.recent = RecentView(self.tab2)

        self.summary.update_sleep_time(5, 30)
        self.detail.update_light_sleep(3, 30)
        self.detail.update_deep_sleep(5, 30)
        self.recent.chart.update([60 * 8, 60 * 5 + 45, 60 * 3 + 15, 60 * 8 + 15, 60 * 10, 60 * 5, 60 * 3 + 90])

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def translate(self):
        self.summary.sleep_label.set_text(tr('Sleep'))
        self.summary.brief.set_text(tr('Total Duration'))
        self.detail.sleep_label.set_text(tr('Sleep'))
        self.detail.slp_light_brief.set_text(tr('Light-Sleep'))
        self.detail.slp_deep_brief.set_text(tr('Deep-Sleep'))
        self.recent.title.set_text(tr('Last 7 days of sleep'))

    def update_time(self, now):
        self.summary.update_time(now.hour, now.minute, now.second)
        self.detail.update_time(now.hour, now.minute, now.second)

    def update_sleep_time(self, data):
        self.summary.update_sleep_time(data['hour'], data['minute'])

    def update_recent_sleep_time(self, data):
        self.recent.chart.update(data)
