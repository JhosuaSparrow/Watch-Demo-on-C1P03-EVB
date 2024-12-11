import lvgl as lv
import sys_bus
from usr.qframe import CurrentApp
from usr.qframe.datetime import DateTime
from usr.topics import LOAD_ADD_ALARMS_VIEW, LOAD_LIST_ALARMS_VIEW
from .language import tr
from .font import Font


WEEKDAY_BRIEF_MAP = {
    0: 'Sun',
    1: 'Mon',
    2: 'Tue',
    3: 'Web',
    4: 'Thu',
    5: 'Fri',
    6: 'Sat',
}


class AddAlarmsView(lv.obj):
    ADD_ALARM_ICON = 'E:/media/alarm/clock_icon5.png'

    def __init__(self, **kwargs):
        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_pos(-10, 10)

        self.bg = lv.canvas(self)
        self.bg.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.bg.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.bg.center()

        self.add_alarm_img = lv.img(self.bg)
        self.add_alarm_img.set_src(self.ADD_ALARM_ICON)
        self.add_alarm_img.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_alarm_img.add_event_cb(
            lambda event: lv.scr_load(SetAlarmTimeView()),
            lv.EVENT.CLICKED,
            None
        )

        self.text = lv.label(self.bg)
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.text.set_text(tr('Add an alarm'))

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        type(self).delete(self)


class ItemView(lv.obj):
    
    def __init__(self, parent, **kwargs):
        self.index = kwargs.get('index')
        self.alarm = kwargs.get('alarm')

        super().__init__(parent)
        self.set_size(230, 100)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_border_width(0, lv.PART.MAIN)

        self.time_text = lv.label(self)
        self.time_text.set_text('{:02d}:{:02d}'.format(self.alarm.hour, self.alarm.minute))
        self.time_text.add_style(Font.get('lv_font_22'), lv.PART.MAIN)
        self.time_text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_text.set_style_align(lv.ALIGN.TOP_LEFT, lv.PART.MAIN)

        self.enable_switch = lv.switch(self)
        self.enable_switch.set_size(68, 34)
        self.enable_switch.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        if self.alarm.valid:
            self.enable_switch.add_state(lv.STATE.CHECKED)
        else:
            self.enable_switch.clear_state(lv.STATE.CHECKED)
        self.enable_switch.add_event_cb(self.sw_event_cb, lv.EVENT.VALUE_CHANGED, None)

        self.time_text = lv.label(self)
        self.time_text.set_size(200, 40)
        self.time_text.set_text('{}'.format(', '.join([WEEKDAY_BRIEF_MAP[_] for _ in self.alarm.weekdays])))
        self.time_text.add_style(Font.get('lv_font_22'), lv.PART.MAIN)
        self.time_text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_text.set_style_align(lv.ALIGN.BOTTOM_LEFT, lv.PART.MAIN)

        self.add_event_cb(lambda event: print('{} index({}) clicked!!!'.format(type(self).__name__, self.index)), lv.EVENT.CLICKED, None)

    def sw_event_cb(self, event):
        self.alarm.valid = self.enable_switch.has_state(lv.STATE.CHECKED)
        CurrentApp().alarm_service.save()


class ListAlarmsView(lv.obj):
    ADD_ALARM_ICON = 'E:/media/alarm/clock_icon5.png'

    def __init__(self, **kwargs):
        self.alarms = kwargs.get('alarms', [])

        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)

        self.bg = lv.canvas(self)
        self.bg.set_size(240, 260)
        self.bg.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.bg.remove_style(None, lv.PART.SCROLLBAR)
        self.bg.set_style_border_width(0, lv.PART.MAIN)
        self.bg.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.bg.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START)
        self.bg.center()

        self.item_views = []
        for index, alarm in enumerate(self.alarms):
            item_view = ItemView(self.bg, index=index, alarm=alarm)
            self.item_views.append(item_view)

        self.add_btn = lv.btn(self)
        self.add_btn.set_size(230, 60)
        self.add_btn.set_style_bg_color(lv.color_hex(0x444444), lv.PART.MAIN)
        self.add_btn.set_style_align(lv.ALIGN.BOTTOM_MID, lv.PART.MAIN)
        self.add_btn_label = lv.label(self.add_btn)
        self.add_btn_label.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.add_btn_label.set_text(tr('Add'))
        self.add_btn_label.center()

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        type(self).delete(self)


class SetAlarmTimeView(lv.obj):

    def __init__(self, info=None):
        self.info = info or {}  # {'index': 0, 'minute': 42, 'weekdays': (3,), 'hour': 16}}

        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.SPACE_BETWEEN)

        self.op_btn = lv.btn(self)
        self.op_btn.set_size(120, 50)
        self.op_btn.set_style_pad_all(0, 0)
        self.op_btn.set_style_align(lv.ALIGN.TOP_LEFT, lv.PART.MAIN)
        self.op_btn.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.op_btn.set_style_shadow_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.op_btn_label = lv.label(self.op_btn)
        self.op_btn_label.set_text('< ' + tr('Set time'))
        self.op_btn_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.op_btn.add_event_cb(self.op_btn_cb, lv.EVENT.CLICKED, None)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)

        self.bg = lv.canvas(self)
        self.bg.set_size(240, 210)
        self.bg.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.bg.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.bg.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.roller_hours = lv.roller(self.bg)
        self.roller_hours.set_options("\n".join(['{:02d}'.format(hour) for hour in range(24)]), lv.roller.MODE.NORMAL)
        self.roller_hours.set_visible_row_count(5)
        self.roller_hours.add_style(Font.get('lv_font_32'), lv.PART.SELECTED)
        self.roller_hours.set_style_border_width(0, lv.PART.MAIN)
        self.roller_hours.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.roller_hours.set_style_text_opa(lv.OPA._80, lv.PART.MAIN)
        self.roller_hours.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED)
        self.roller_hours.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.roller_hours.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.SELECTED)
        self.roller_hours.add_event_cb(
            lambda event: self.info.update({'hour': self.roller_hours.get_selected()}),
            lv.EVENT.VALUE_CHANGED,
            None
        )

        self.roller_minutes = lv.roller(self.bg)
        self.roller_minutes.set_options("\n".join(['{:02d}'.format(hour) for hour in range(60)]), lv.roller.MODE.NORMAL)
        self.roller_minutes.set_visible_row_count(5)
        self.roller_minutes.add_style(Font.get('lv_font_32'), lv.PART.SELECTED)
        self.roller_minutes.set_style_border_width(0, lv.PART.MAIN)
        self.roller_minutes.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.roller_minutes.set_style_text_opa(lv.OPA._80, lv.PART.MAIN)
        self.roller_minutes.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED)
        self.roller_minutes.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.roller_minutes.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.SELECTED)
        self.roller_minutes.add_event_cb(
            lambda event: self.info.update({'minute': self.roller_minutes.get_selected()}),
            lv.EVENT.VALUE_CHANGED,
            None
        )

        self.button_check = lv.btn(self)
        self.button_check.set_size(230, 60)
        self.button_check.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.button_check.add_event_cb(self.button_check_cb, lv.EVENT.CLICKED, None)
        self.button_check_label = lv.label(self.button_check)
        self.button_check_label.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.button_check_label.set_text(tr('Next Step'))
        self.button_check_label.center()

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({}), recv info: {}'.format(
            type(self).__name__,
            id(self),
            event.get_code(),
            self.info
        ))
        if not self.info:
            now = DateTime.now()
            self.info.update({'index': -1, 'minute': now.minute, 'weekdays': [], 'hour': now.hour})  # -1 means a new alarm
        self.roller_hours.set_selected(self.info['hour'], lv.ANIM.OFF)
        self.roller_minutes.set_selected(self.info['minute'], lv.ANIM.OFF)

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        type(self).delete(self)

    def op_btn_cb(self, event):
        print('{} op_btn_cb'.format(type(self).__name__))
        alarms = []
        if alarms:
            lv.scr_load(ListAlarmsView(alarms=alarms))
        else:
            lv.scr_load(AddAlarmsView())

    def button_check_cb(self, event):
        print('{} button_check_cb with info: {}'.format(type(self).__name__, self.info))
        lv.scr_load(SetAlarmWeekdayView(info=self.info))


class SetAlarmWeekdayView(lv.obj):

    def __init__(self, info=None):
        self.info = info

        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.SPACE_BETWEEN)

        self.op_btn = lv.btn(self)
        self.op_btn.set_size(120, 50)
        self.op_btn.set_style_pad_all(0, 0)
        self.op_btn.set_style_align(lv.ALIGN.TOP_LEFT, lv.PART.MAIN)
        self.op_btn.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.op_btn.set_style_shadow_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.op_btn.add_event_cb(
            lambda event: lv.scr_load(SetAlarmTimeView(info=self.info)),
            lv.EVENT.CLICKED,
            None
        )
        self.op_btn_label = lv.label(self.op_btn)
        self.op_btn_label.set_text('< ' + tr('Set time'))
        self.op_btn_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)

        self.time_label = lv.label(self)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))
        self.time_label.set_style_align(lv.ALIGN.TOP_RIGHT, lv.PART.MAIN)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)

        self.bg = lv.canvas(self)
        self.bg.set_size(240, 210)
        self.bg.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.bg.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
        self.bg.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.weekday_btn_dict = {}
        for weekday in range(7):
            btn = lv.btn(self.bg)
            btn.set_size(76, 38)
            btn.set_style_radius(20, lv.PART.MAIN)
            btn.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN)
            btn.set_style_shadow_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            btn.add_event_cb(self.weekday_btn_clicked_cb, lv.EVENT.CLICKED, None)
            btn_label = lv.label(btn)
            btn_label.set_text(WEEKDAY_BRIEF_MAP[weekday])
            btn_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
            btn_label.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
            btn_label.center()
            if weekday in (2, 5):
                btn.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
            self.weekday_btn_dict[id(btn)] = [btn, weekday, False]

        self.button_check = lv.btn(self)
        self.button_check.set_size(230, 60)
        self.button_check.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.button_check.add_event_cb(self.button_check_cb, lv.EVENT.CLICKED, None)
        self.button_check_label = lv.label(self.button_check)
        self.button_check_label.add_style(Font.get('lv_font_32'), lv.PART.MAIN)
        self.button_check_label.set_text(tr('Ok'))
        self.button_check_label.center()

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({}), recv info: {}'.format(
            type(self).__name__,
            id(self),
            event.get_code(),
            self.info
        ))
        if self.info:
            for key in self.weekday_btn_dict.keys():
                if self.weekday_btn_dict[key][1] in self.info['weekdays']:
                    self.weekday_btn_dict[key][2] = True
                    self.weekday_btn_dict[key][0].set_style_bg_color(lv.palette_main(lv.PALETTE.ORANGE), lv.PART.MAIN)

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        type(self).delete(self)

    def weekday_btn_clicked_cb(self, event):
        key = id(event.get_target())
        btn, weekday, flag = self.weekday_btn_dict[key]
        is_checked = not flag
        print('{} weekday_btn_clicked_cb, weekday: {}, is_checked: {}'.format(type(self).__name__, weekday, is_checked))
        btn.set_style_bg_color(
            lv.palette_main(lv.PALETTE.ORANGE) if is_checked else lv.palette_main(lv.PALETTE.GREY),
            lv.PART.MAIN
        )
        self.weekday_btn_dict[key][2] = is_checked
        if is_checked:
            self.info['weekdays'].append(weekday)
        else:
            if weekday in self.info['weekdays']:
                self.info['weekdays'].remove(weekday)

    def button_check_cb(self, event):
        print('{} button_check_cb with info: {}'.format(type(self).__name__, self.info))


sys_bus.subscribe(LOAD_ADD_ALARMS_VIEW, lambda topic, kwargs: lv.scr_load(AddAlarmsView(**kwargs)))
sys_bus.subscribe(LOAD_LIST_ALARMS_VIEW, lambda topic, kwargs: lv.scr_load(ListAlarmsView(**kwargs)))
