import sys_bus
import lvgl as lv
from usr.ui.language import tr
from usr.ui.font import Font


class SummaryView(lv.canvas):
    BLOOD_PRESSURE_ICON_SRC = 'E:/media/blood_pressure/bp_dy_icon_{:02d}.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START)

        self.content1 = lv.canvas(self)
        self.content1.set_size(232, 280)
        self.content1.set_layout(lv.LAYOUT_FLEX.value)
        self.content1.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content1.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.press_label = lv.label(self.content1)
        self.press_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.press_label.set_text(tr('Blood Pressure'))

        self.time_label = lv.label(self.content1)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        # self.press_indicator = lv.animimg(self.content1)
        # anim_imgs = []
        # for i in range(1, 3):
        #     with open(self.BLOOD_PRESSURE_ICON_SRC.format(i), 'rb') as f:
        #         data = f.read()
        #         anim_imgs.append(
        #             lv.img_dsc_t(
        #                 {
        #                     'data_size': len(data),
        #                     'data': data
        #                 }
        #             )
        #         )
        # self.press_indicator.set_src(anim_imgs, len(anim_imgs))
        # self.press_indicator.set_duration(1000)
        # self.press_indicator.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
        self.press_indicator = lv.img(self.content1)
        self.press_indicator.set_src(self.BLOOD_PRESSURE_ICON_SRC.format(1))
        self.press_indicator.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        # self.press_indicator.start()

        self.remaining = lv.label(self.content1)
        self.remaining.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.remaining.set_text('{}s'.format(30))
        self.remaining.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.remaining.add_style(Font.get('lv_font_18'), lv.PART.MAIN)

        self.value = lv.label(self.content1)
        self.value.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.value.set_text('{}'.format(38))
        self.value.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.value.add_style(Font.get('lv_font_32'), lv.PART.MAIN)

        self.text = lv.label(self.content1)
        self.text.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        self.text.set_text(tr('Checking'))
        self.text.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.text.add_style(Font.get('lv_font_32'), lv.PART.MAIN)

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_pos(1, 2)

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))


class ChartView(lv.img):
    PRESS_BG_SRC = 'E:/media/blood_pressure/bp_bg.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_src(self.PRESS_BG_SRC)

        self.columns = []
        for i in range(24):
            obj = lv.obj(self)
            obj.set_size(4, 0)
            obj.set_pos(35 + (i * 8), 6)
            obj.set_style_radius(20, lv.PART.MAIN)
            obj.set_style_border_width(0, lv.PART.MAIN)
            obj.set_style_bg_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN)
            self.columns.append(obj)

    def update(self, hour, lowest, highest):
        self.columns[hour].set_pos(35 + hour * 8, 6 + 200 - highest)
        self.columns[hour].set_height(highest - lowest)


class DetailView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/common/activity_data_18x25.png'
    UNIT_IMG_SRC = 'E:/media/pressdata/bo_data_icon3.png'
    SIDE_BAR_BG = 'E:/media/common/bar_6x36.png'
    SIDE_BAR_INDICATOR = 'E:/media/common/bar_4x16.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.content1 = lv.canvas(self)
        self.content1.set_size(232, 280)
        self.content1.set_layout(lv.LAYOUT_FLEX.value)
        self.content1.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.content1.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.press_label = lv.label(self.content1)
        self.press_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.press_label.set_text(tr('Pressure'))

        self.time_label = lv.label(self.content1)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.chart = ChartView(self.content1)

        self.side_bar_bg = lv.img(self)
        self.side_bar_bg.set_src(self.SIDE_BAR_BG)
        self.side_bar = lv.img(self.side_bar_bg)
        self.side_bar.set_src(self.SIDE_BAR_INDICATOR)
        self.side_bar.set_pos(1, 18)

    def update_time(self, hour, minute, second):
        self.time_label.set_text('{:02d}:{:02d}'.format(hour, minute))


class BloodPressureView(lv.tabview):

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
            self.detail.chart.update(hour, 80, 130)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_time(self, now):
        self.summary.update_time(now.hour, now.minute, now.second)
        self.detail.update_time(now.hour, now.minute, now.second)
