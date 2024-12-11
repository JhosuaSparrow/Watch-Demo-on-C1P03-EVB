import sys_bus
import voiceCall
import lvgl as lv
from .font import Font
from .language import tr
from usr.topics import (
    FUNC_VOLTE_CONNECTED,
    LOAD_INCOMING_CALL_VIEW,
    LOAD_DIALING_VIEW,
    LOAD_MAIN_VIEW
)


class CallingView(lv.obj):
    CALL_ICON_1 = 'E:/media/telephone/call_icon1.png'
    CALL_ICON_2_1 = 'E:/media/telephone/call_icon2_1.png'
    CALL_ICON_2_2 = 'E:/media/telephone/call_icon2_2.png'
    CALL_ICON_2_3 = 'E:/media/telephone/call_icon2_3.png'
    CALL_ICON_3_1 = 'E:/media/telephone/call_icon3_1.png'
    CALL_ICON_3_2 = 'E:/media/telephone/call_icon3_2.png'
    CALL_ICON_4_1 = 'E:/media/telephone/call_icon4_1.png'
    CALL_ICON_4_2 = 'E:/media/telephone/call_icon4_2.png'

    def __init__(self, phone_number='+8618588269037', call_type='answer'):
        self.call_type = call_type  # answer or start
        self.phone_number = phone_number
        self.timer = None

        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_border_width(0, lv.PART.MAIN)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_pos(-10, 10)

        self.bg = lv.canvas(self)
        self.bg.set_size(240, 280)
        self.bg.set_pos(0, 40)
        self.bg.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.bg.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.name = lv.label(self.bg)
        self.name.set_text(tr('unknown'))
        self.name.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.name.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.phone_label = lv.label(self.bg)
        self.phone_label.set_text(self.phone_number)
        self.phone_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.phone_label.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.phone_label.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.text = lv.label(self.bg)
        self.text.set_text(tr('calling'))
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.call_silent_bg = lv.img(self.bg)
        self.call_silent_bg.set_src(self.CALL_ICON_4_2)
        self.call_silent_bg.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_silent_bg.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.call_silent = lv.img(self.call_silent_bg)
        self.call_silent.set_src(self.CALL_ICON_4_1)
        self.call_silent.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_silent.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        self.call_accept = lv.img(self.bg)
        self.call_accept.set_src(self.CALL_ICON_3_2)
        self.call_accept.add_flag(lv.obj.FLAG.CLICKABLE)

        self.call_voice_bg = lv.img(self.bg)
        self.call_voice_bg.set_src(self.CALL_ICON_2_2)
        self.call_voice_bg.add_flag(lv.obj.FLAG.CLICKABLE)

        self.call_voice = lv.img(self.call_voice_bg)
        self.call_voice.set_src(self.CALL_ICON_2_3)
        self.call_voice.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_voice.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        self.call_reject = lv.img(self.bg)
        self.call_reject.set_src(self.CALL_ICON_1)
        self.call_reject.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_reject.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.call_reject.add_event_cb(self.call_reject_cb, lv.EVENT.CLICKED, None)

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        sys_bus.subscribe(FUNC_VOLTE_CONNECTED, self.func_volte_connected_cb)
        if self.call_type == 'answer':
            voiceCall.callAnswer()
        else:
            voiceCall.callStart(self.phone_number)

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        sys_bus.unsubscribe(FUNC_VOLTE_CONNECTED, self.func_volte_connected_cb)
        voiceCall.callEnd()
        if self.timer:
            self.timer.set_repeat_count(0)
        type(self).delete(self)

    def call_reject_cb(self, event):
        print('{} call_reject_cb'.format(type(self).__name__))
        sys_bus.publish(LOAD_MAIN_VIEW, {})

    def func_volte_connected_cb(self, topic, data):
        total_seconds = 0

        def timer_cb(timer):
            nonlocal total_seconds
            self.text.set_text('{:02d}:{:02d}'.format(total_seconds // 60, total_seconds % 60))
            total_seconds += 1

        self.timer = lv.timer_create(timer_cb, 1000, None)


class InComingCallView(lv.obj):
    CALL_ACCEPT_ICON = 'E:/media/telephone/call_icon01.png'
    CALL_REJECT_ICON = 'E:/media/telephone/call_icon02.png'

    def __init__(self, **kwargs):
        self.phone_number = kwargs.get('phone_number', 'N/A')

        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_border_width(0, lv.PART.MAIN)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_pos(-10, 10)

        self.bg = lv.canvas(self)
        self.bg.set_size(240, 280)
        self.bg.set_pos(0, 40)
        self.bg.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.bg.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.SPACE_EVENLY)

        self.name = lv.label(self.bg)
        self.name.set_text(tr('unknown'))
        self.name.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.name.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.phone_label = lv.label(self.bg)
        self.phone_label.set_text(self.phone_number)
        self.phone_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.phone_label.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.phone_label.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.text = lv.label(self.bg)
        self.text.set_text(tr('incoming call'))
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.add_style(Font.get('lv_font_24'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.call_accept = lv.img(self.bg)
        self.call_accept.set_src(self.CALL_ACCEPT_ICON)
        self.call_accept.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_accept.set_style_align(lv.ALIGN.BOTTOM_LEFT, lv.PART.MAIN)
        self.call_accept.set_y(-60)
        self.call_accept.add_event_cb(self.call_accept_cb, lv.EVENT.CLICKED, None)
        self.call_accept.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.call_reject = lv.img(self.bg)
        self.call_reject.set_src(self.CALL_REJECT_ICON)
        self.call_reject.add_flag(lv.obj.FLAG.CLICKABLE)
        self.call_reject.set_style_align(lv.ALIGN.BOTTOM_RIGHT, lv.PART.MAIN)
        self.call_reject.set_y(-60)
        self.call_reject.add_event_cb(self.call_reject_cb, lv.EVENT.CLICKED, None)

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

        self.is_accepted = False

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        if not self.is_accepted:
            voiceCall.callEnd()
        type(self).delete(self)

    def call_reject_cb(self, event):
        print('{} call_reject_cb'.format(type(self).__name__))
        sys_bus.publish(LOAD_MAIN_VIEW, {})

    def call_accept_cb(self, event):
        print('{} call_accept_cb'.format(type(self).__name__))
        self.is_accepted = True
        lv.scr_load(CallingView(phone_number=self.phone_number, call_type='answer'))


class NumberView(lv.obj):

    def __init__(self, parent, number=0):
        super().__init__(parent)
        self.set_size(70, 60)
        self.set_style_radius(10, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_hex(0x444444), lv.PART.MAIN)
        self.set_style_bg_color(lv.palette_main(lv.PALETTE.ORANGE), lv.PART.MAIN | lv.STATE.PRESSED)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)

        self.num = lv.label(self)
        self.num.set_text(str(number))
        self.num.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.num.add_style(Font.get('lv_font_32'), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.num.center()


class DialingView(lv.obj):
    ACCEPT_ICON = 'E:/media/telephone/Dialpad_icon1_2.png'
    CANCEL_ICON = 'E:/media/telephone/Dialpad_icon2_2.png'

    def __init__(self, **kwargs):
        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.CENTER)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        self.phone_text = lv.label(self)
        self.phone_text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.phone_text.add_style(Font.get('lv_font_24'), lv.PART.MAIN)
        self.phone_text.set_text('')

        self.n1 = NumberView(self, number=1)
        self.n1.add_event_cb(lambda event: self.__number_clicked_cb(event, 1), lv.EVENT.CLICKED, None)
        self.n1.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.n2 = NumberView(self, number=2)
        self.n2.add_event_cb(lambda event: self.__number_clicked_cb(event, 2), lv.EVENT.CLICKED, None)
        self.n3 = NumberView(self, number=3)
        self.n3.add_event_cb(lambda event: self.__number_clicked_cb(event, 3), lv.EVENT.CLICKED, None)

        self.n4 = NumberView(self, number=4)
        self.n4.add_event_cb(lambda event: self.__number_clicked_cb(event, 4), lv.EVENT.CLICKED, None)
        self.n4.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.n5 = NumberView(self, number=5)
        self.n5.add_event_cb(lambda event: self.__number_clicked_cb(event, 5), lv.EVENT.CLICKED, None)
        self.n6 = NumberView(self, number=6)
        self.n6.add_event_cb(lambda event: self.__number_clicked_cb(event, 6), lv.EVENT.CLICKED, None)

        self.n7 = NumberView(self, number=7)
        self.n7.add_event_cb(lambda event: self.__number_clicked_cb(event, 7), lv.EVENT.CLICKED, None)
        self.n7.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.n8 = NumberView(self, number=8)
        self.n8.add_event_cb(lambda event: self.__number_clicked_cb(event, 8), lv.EVENT.CLICKED, None)
        self.n9 = NumberView(self, number=9)
        self.n9.add_event_cb(lambda event: self.__number_clicked_cb(event, 9), lv.EVENT.CLICKED, None)

        self.cancel = lv.img(self)
        self.cancel.set_src(self.CANCEL_ICON)
        self.cancel.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK | lv.obj.FLAG.CLICKABLE)
        self.cancel.add_event_cb(lambda event: self.__number_clicked_cb(event, -1), lv.EVENT.CLICKED, None)

        self.n0 = NumberView(self, number=0)
        self.n0.add_event_cb(lambda event: self.__number_clicked_cb(event, 0), lv.EVENT.CLICKED, None)

        self.accept = lv.img(self)
        self.accept.set_src(self.ACCEPT_ICON)
        self.accept.add_flag(lv.obj.FLAG.CLICKABLE)
        self.accept.add_event_cb(lambda event: self.__number_clicked_cb(event, -2), lv.EVENT.CLICKED, None)

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        type(self).delete(self)

    def __number_clicked_cb(self, event, number):
        if number >= 0:
            self.phone_text.set_text(self.phone_text.get_text() + str(number))
        else:
            if number == -1:
                self.phone_text.set_text(self.phone_text.get_text()[:-1])
            else:
                print('{} __number_clicked_cb accept...phone number: {}'.format(type(self).__name__, self.phone_text.get_text()))
                lv.scr_load(CallingView(phone_number=self.phone_text.get_text(), call_type='start'))


sys_bus.subscribe(LOAD_INCOMING_CALL_VIEW, lambda topic, kwargs: lv.scr_load(InComingCallView(**kwargs)))
sys_bus.subscribe(LOAD_DIALING_VIEW, lambda topic, kwargs: lv.scr_load(DialingView(**kwargs)))
