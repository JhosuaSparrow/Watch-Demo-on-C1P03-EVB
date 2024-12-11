"""功能界面，活动步数"""
import lvgl as lv
import sys_bus
from ..language import tr
from ..font import Font


class SummaryView(lv.canvas):
    STEP_ICON_SRC = 'E:/media/activity/step_icon1.png'
    BAR_ICON_SRC = 'E:/media/activity/step_progress_0.png'
    KM_ICON_SRC = 'E:/media/activity/step_icon2.png'
    KCAL_ICON_SRC = 'E:/media/activity/step_icon3.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        self.layout = lv.canvas(self)
        self.layout.set_size(240, 280)
        self.layout.set_pos(0, 0)
        self.layout.set_layout(lv.LAYOUT_FLEX.value)
        self.layout.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.layout.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER)
        self.layout.set_style_pad_row(15, lv.PART.MAIN)
        self.layout.set_style_pad_column(5, lv.PART.MAIN)

        self.step_icon = lv.img(self.layout)
        self.step_icon.set_src(self.STEP_ICON_SRC)

        self.step_digit = lv.label(self.layout)
        self.step_digit.add_style(Font.get('lv_font_32'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.step_digit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.step_digit.set_text('0')

        self.step_unit = lv.label(self.layout)
        self.step_unit.set_text(tr('Steps'))
        self.step_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.step_unit.add_style(Font.get('lv_font_22'), lv.PART.MAIN)

        self.bar = lv.img(self.layout)
        self.bar.set_src(self.BAR_ICON_SRC)
        self.bar.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.achievement_label = lv.label(self.layout)
        self.achievement_label.set_text('{}: {:d}%'.format(tr('Achievement Rate'), 0))
        self.achievement_label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.achievement_label.add_style(Font.get('lv_font_22'), lv.PART.MAIN)
        self.achievement_label.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.km_icon = lv.img(self.layout)
        self.km_icon.set_src(self.KM_ICON_SRC)
        self.km_icon.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.km_digit = lv.label(self.layout)
        self.km_digit.set_text('00.0')
        self.km_digit.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.km_digit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)

        self.km_unit = lv.label(self.layout)
        self.km_unit.set_text(tr('km'))
        self.km_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.km_unit.add_style(Font.get('lv_font_22'), lv.PART.MAIN)

        self.kcal_icon = lv.img(self.layout)
        self.kcal_icon.set_src(self.KCAL_ICON_SRC)
        self.kcal_icon.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.kcal_digit = lv.label(self.layout)
        self.kcal_digit.set_text('0000')
        self.kcal_digit.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.kcal_digit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)

        self.kcal_unit = lv.label(self.layout)
        self.kcal_unit.set_text(tr('kcal'))
        self.kcal_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.kcal_unit.add_style(Font.get('lv_font_22'), lv.PART.MAIN)

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 36)
        self.side_bar_bg.set_pos(232, 122)
        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 2)

    def update_step(self, value):
        self.step_digit.set_text(str(value))

    def update_km(self, value):
        self.km_digit.set_text(str(value))

    def update_kcal(self, value):
        self.kcal_digit.set_text(str(value))

    def update_achievement_rate(self, rate):
        # rate: 0~100
        self.achievement_label.set_text('{}: {:d}%'.format(tr('Achievement Rate'), rate))
        # level: 0~30
        self.bar.set_src('E:/media/activity/step_progress_{}.png'.format(int(rate / 3.3)))


class ActivityChart(lv.canvas):
    ACT_PRG_SRC = 'E:/media/activity/activity_prg.png'
    ACT_SPLIT_SRC = 'E:/media/activity/activity_split_line.png'
    DIGIT_SRC = 'E:/media/common/step_data_10x12.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240-3-16, 280-105-62)
        self.set_pos(3, 62)

        self.top_number_list = []
        for i in range(5):
            img = lv.img(self)
            img.set_src(self.DIGIT_SRC)
            img.set_size(10, 12)
            img.set_pos(i * 10, 0)
            img.set_offset_y(0)
            self.top_number_list.append(img)
        self.top_number_list[0].set_offset_y(-12*5)

        self.mid_number_list = []
        for i in range(5):
            img = lv.img(self)
            img.set_src(self.DIGIT_SRC)
            img.set_size(10, 12)
            img.set_pos(i * 10, 37 + 12)
            img.set_offset_y(0)
            self.mid_number_list.append(img)
        self.mid_number_list[0].set_offset_y(-12 * 2)
        self.mid_number_list[1].set_offset_y(-12 * 5)

        self.bottom_number = lv.img(self)
        self.bottom_number.set_src(self.DIGIT_SRC)
        self.bottom_number.set_size(10, 12)
        self.bottom_number.set_pos(40, 40+37+24)
        self.bottom_number.set_offset_y(0)

        self.split_line1 = lv.img(self)
        self.split_line1.set_src(self.ACT_SPLIT_SRC)
        self.split_line1.set_size(166, 1)
        self.split_line1.set_pos(5+12*5, 6)

        self.split_line2 = lv.img(self)
        self.split_line2.set_src(self.ACT_SPLIT_SRC)
        self.split_line2.set_size(166, 1)
        self.split_line2.set_pos(5+12*5, 6+50)

        self.split_line3 = lv.img(self)
        self.split_line3.set_src(self.ACT_SPLIT_SRC)
        self.split_line3.set_size(166, 1)
        self.split_line3.set_pos(5+12*5, 6+50+50)

        self.columns = []
        for i in range(7):
            obj = lv.obj(self)
            obj.set_style_radius(0, lv.PART.MAIN)
            obj.set_style_border_width(0, lv.PART.MAIN)
            obj.set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), lv.PART.MAIN)
            obj.set_size(8, 0)
            obj.set_pos(40 + 9 + 10 + (24 * i), 6+50+50)
            self.columns.append(obj)

    def update(self, data_list):
        for index, column in enumerate(self.columns):
            height = data_list[index] // 500  # 500 steps per pix
            column.set_height(height)
            column.set_y(106 - height)


class RecentView(lv.canvas):
    BRIEF_IMG_SRC = 'E:/media/activity/activity_bg.png'
    DAY_IMG_SRC = 'E:/media/common/data_step_22x31.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        self.title = lv.label(self)
        self.title.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.title.set_size(204, 25)
        self.title.set_pos(20, 15)
        self.title.set_text(tr('Last 7 days steps'))

        self.brief = lv.img(self)
        self.brief.set_src(self.BRIEF_IMG_SRC)
        self.brief.set_size(224, 80)
        self.brief.set_pos(8, 180)

        self.days = lv.img(self.brief)
        self.days.set_src(self.DAY_IMG_SRC)
        self.days.set_size(22, 31)
        self.days.set_pos(84, 8)
        self.days.set_offset_y(0)

        self.days_unit = lv.label(self.brief)
        self.days_unit.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.days_unit.set_size(60, 24)
        self.days_unit.set_pos(110, 15)
        self.days_unit.set_text(tr('day'))

        self.desc = lv.label(self.brief)
        self.desc.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.desc.set_size(136, 24)
        self.desc.set_pos(44, 46)
        self.desc.set_text(tr('Up to standard'))

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar_bg.set_size(6, 36)
        self.side_bar_bg.set_pos(232, 122)

        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_size(4, 16)
        self.side_bar.set_pos(1, 18)

        self.chart = ActivityChart(self)

    def update(self, step_data_list, goal=20000):
        self.chart.update(step_data_list)
        self.days.set_offset_y(-31 * sum((step >= goal for step in step_data_list)))


class ActivityView(lv.tabview):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, lv.DIR.RIGHT, 0)
        self.set_size(240, 320)
        self.set_pos(0, 0)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        # 活动数据
        self.tab0 = self.add_tab("tab0")
        self.tab0.set_style_pad_all(0, lv.PART.MAIN)
        self.summary = SummaryView(self.tab0)

        # 近7天数据
        self.tab1 = self.add_tab("tab1")
        self.tab1.set_style_pad_all(0, lv.PART.MAIN)
        self.recent = RecentView(self.tab1)

        self.summary.update_step(12345)
        self.summary.update_kcal(2500)
        self.summary.update_km(11.1)
        self.summary.update_achievement_rate(80)
        self.recent.update([8000, 10000, 12000, 15000, 20000, 26000, 45000])

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))
