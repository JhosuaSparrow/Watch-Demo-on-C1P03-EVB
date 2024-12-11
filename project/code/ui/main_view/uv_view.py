import sys_bus
import lvgl as lv
from ..language import tr
from ..font import Font


class BarView(lv.canvas):
    BAR_BG_SRC = 'E:/media/uv/UV index_icon_02.png'
    INDICATOR_SRC = 'E:/media/uv/UV index_icon_03.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(180, 23)
        self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.bar_bg = lv.img(self)
        self.bar_bg.set_src(self.BAR_BG_SRC)

        self.indicator_bg = lv.canvas(self)
        self.indicator_bg.set_size(180, 11)
        self.indicator = lv.img(self.indicator_bg)
        self.indicator.set_src(self.INDICATOR_SRC)
        self.indicator.set_pos(0, 0)

    def update(self, level):
        # level: 0~14
        self.indicator.set_pos(12*level, 0)


class UVView(lv.canvas):
    UV_ICON_SRC = 'E:/media/uv/UV index_icon_01.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 320)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        self.uv_label = lv.label(self)
        self.uv_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.uv_label.set_text(tr('UV Index'))

        self.time_label = lv.label(self)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.uv_icon = lv.img(self)
        self.uv_icon.set_src(self.UV_ICON_SRC)
        self.uv_icon.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.value = lv.label(self)
        self.value.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.value.set_text('{}'.format('-'))
        self.value.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.value.add_style(Font.get('lv_font_32'), lv.PART.MAIN)

        self.text = lv.label(self)
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.set_text(tr('Checking'))
        self.text.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.text.add_style(Font.get('lv_font_32'), lv.PART.MAIN)

        self.bar = BarView(self)
        self.bar.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.update_uv_index(5)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_time(self, now):
        self.time_label.set_text('{:02d}:{:02d}'.format(now.hour, now.minute))

    def update_uv_index(self, index):
        self.bar.update(index)
        self.value.set_text(str(index))
        if index <= 2:
            self.text.set_text('Weaker')
        elif index <= 5:
            self.text.set_text('Moderate')
        elif index <= 7:
            self.text.set_text('High')
        elif index <= 10:
            self.text.set_text('Very High')
        else:
            self.text.set_text('Extreme')
