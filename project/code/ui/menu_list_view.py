import sys_bus
import lvgl as lv
from usr.qframe.collections import Singleton
from .language import tr
from .font import Font
from usr.topics import LOAD_MENU_LIST_VIEW, LOAD_DIALING_VIEW, LOAD_ADD_ALARMS_VIEW, LOAD_LIST_ALARMS_VIEW


class ListItemView(lv.img):
    MENU_BG_ICON = 'E:/media/menu_list/menu_icon_01.png'
    DEFAULT_ICON = 'E:/media/menu_list/func_list_telephone.png'

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.set_src(self.MENU_BG_ICON)

        self.icon = lv.img(self)
        self.icon.set_src(kwargs.get('icon', self.DEFAULT_ICON))
        self.icon.set_style_align(lv.ALIGN.LEFT_MID, lv.PART.MAIN)
        self.icon.set_x(7)

        self.text = lv.label(self)
        self.text.set_text(kwargs.get('text', ''))
        self.text.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.text.add_style(Font.get('lv_font_24'), lv.PART.MAIN)
        self.text.set_style_align(lv.ALIGN.LEFT_MID, lv.PART.MAIN)
        self.text.set_x(7+58+20)

        self.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_event_cb(kwargs.get('item_click_cb', lambda _: None), lv.EVENT.CLICKED, None)


@Singleton
class MenuListView(lv.obj):
    TELEPHONE_ICON = 'E:/media/menu_list/func_list_telephone.png'
    ALARM_ICON = 'E:/media/menu_list/func_list_Alarm clock.png'
    FLASHLIGHT_ICON = 'E:/media/menu_list/func_list_flashlight.png'
    AUDIO_ICON = 'E:/media/menu_list/func_list_audio.png'
    ACTIVITY_ICON = 'E:/media/menu_list/func_list_activity.png'
    EXERCISE_ICON = 'E:/media/menu_list/func_list_exercise.png'
    SET_ICON = 'E:/media/menu_list/func_list_set.png'

    def __init__(self, **kwargs):
        super().__init__(None)
        self.set_size(240, 320)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)

        self.telephone = ListItemView(self, icon=self.TELEPHONE_ICON, text=tr('Telephone'), item_click_cb=self.telephone_cb)
        self.alarm = ListItemView(self, icon=self.ALARM_ICON, text=tr('Alarm'), item_click_cb=self.alarm_cb)
        self.flashlight = ListItemView(self, icon=self.FLASHLIGHT_ICON, text=tr('Flashlight'), item_click_cb=self.flashlight_cb)
        self.audio = ListItemView(self, icon=self.AUDIO_ICON, text=tr('Audio'), item_click_cb=self.audio_cb)
        self.activity = ListItemView(self, icon=self.ACTIVITY_ICON, text=tr('Activity'), item_click_cb=self.activity_cb)
        self.exercise = ListItemView(self, icon=self.EXERCISE_ICON, text=tr('Exercise'), item_click_cb=self.exercise_cb)
        self.settings = ListItemView(self, icon=self.SET_ICON, text=tr('Settings'), item_click_cb=self.settings_cb)

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))
        self.scroll_to_y(0, lv.PART.MAIN)

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def telephone_cb(self, event):
        print('{} telephone_cb'.format(type(self).__name__))
        sys_bus.publish(LOAD_DIALING_VIEW, {})

    def alarm_cb(self, event):
        print('{} alarm_cb'.format(type(self).__name__))
        from usr.extensions import alarm_service
        if alarm_service.alarms:
            sys_bus.publish(LOAD_LIST_ALARMS_VIEW, {'alarms': alarm_service.alarms})
        else:
            sys_bus.publish(LOAD_ADD_ALARMS_VIEW, {})

    def flashlight_cb(self, event):
        print('{} flashlight_cb'.format(type(self).__name__))

    def audio_cb(self, event):
        print('{} audio_cb'.format(type(self).__name__))

    def activity_cb(self, event):
        print('{} activity_cb'.format(type(self).__name__))

    def exercise_cb(self, event):
        print('{} exercise_cb'.format(type(self).__name__))

    def settings_cb(self, event):
        print('{} settings_cb'.format(type(self).__name__))


sys_bus.subscribe(LOAD_MENU_LIST_VIEW, lambda topic, kwargs: lv.scr_load(MenuListView(**kwargs)))
