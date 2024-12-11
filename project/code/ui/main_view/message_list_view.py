import sys_bus
import lvgl as lv
from ..language import tr
from ..font import Font


class MessageListView(lv.obj):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.set_style_radius(0, lv.PART.MAIN)
        self.set_style_border_width(0, lv.PART.MAIN)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_pos(-10, 10)

        self.no_message_img = lv.img(self)
        self.no_message_img.set_src('E:/media/message/msg_no_msg.png')
        self.no_message_img.center()

        self.text = lv.label(self)
        self.text.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.set_text(tr('No Message'))
        self.text.center()
        self.text.set_y(60)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))
