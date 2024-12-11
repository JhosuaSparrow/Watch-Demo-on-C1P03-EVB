import sys_bus
import lvgl as lv
from ..font import Font
from ..language import tr


class FunctionsView(lv.obj):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 180)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.set_style_radius(20, lv.PART.MAIN)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.set_grid_dsc_array(
            [75, 75, 75, 75, 75, 75, lv.GRID_TEMPLATE.LAST],
            [75, 75, lv.GRID_TEMPLATE.LAST]
        )

        self.backlight = lv.img(self)
        self.backlight.set_src('E:/media/control_center/backlight/set_backlight_10.png')
        self.backlight.set_grid_cell(
            lv.GRID_ALIGN.START, 0, 1,
            lv.GRID_ALIGN.START, 0, 2
        )

        self.flashlight_bg = lv.img(self)
        self.flashlight_bg.set_src('E:/media/control_center/set_flashlight_02.png')
        self.flashlight_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 1, 1,
            lv.GRID_ALIGN.START, 0, 1
        )
        self.flashlight = lv.img(self.flashlight_bg)
        self.flashlight.set_src('E:/media/control_center/set_flashlight_01.png')
        self.flashlight.add_flag(lv.obj.FLAG.CLICKABLE)
        self.flashlight.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.flashlight.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.flashlight_action),
            lv.EVENT.CLICKED,
            None
        )

        self.lift_bg = lv.img(self)
        self.lift_bg.set_src('E:/media/control_center/set_lift_02.png')
        self.lift_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 2, 1,
            lv.GRID_ALIGN.START, 0, 1
        )
        self.lift = lv.img(self.lift_bg)
        self.lift.set_src('E:/media/control_center/set_lift_01.png')
        self.lift.add_flag(lv.obj.FLAG.CLICKABLE)
        self.lift.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.lift.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.lift_action),
            lv.EVENT.CLICKED,
            None
        )

        self.findphone_bg = lv.img(self)
        self.findphone_bg.set_src('E:/media/control_center/set_findphone_02.png')
        self.findphone_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 3, 1,
            lv.GRID_ALIGN.START, 0, 1
        )
        self.findphone = lv.img(self.findphone_bg)
        self.findphone.set_src('E:/media/control_center/set_findphone_01.png')
        self.findphone.add_flag(lv.obj.FLAG.CLICKABLE)
        self.findphone.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.findphone.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.findphone_action),
            lv.EVENT.CLICKED,
            None
        )

        self.audio_bg = lv.img(self)
        self.audio_bg.set_src('E:/media/control_center/set_audio_02.png')
        self.audio_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 4, 1,
            lv.GRID_ALIGN.START, 0, 1
        )
        self.audio = lv.img(self.audio_bg)
        self.audio.set_src('E:/media/control_center/set_audio_01.png')
        self.audio.add_flag(lv.obj.FLAG.CLICKABLE)
        self.audio.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.audio.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.audio_action),
            lv.EVENT.CLICKED,
            None
        )

        self.setting_bg = lv.img(self)
        self.setting_bg.set_src('E:/media/control_center/set_setting_02.png')
        self.setting_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 5, 1,
            lv.GRID_ALIGN.START, 0, 1
        )
        self.setting = lv.img(self.setting_bg)
        self.setting.set_src('E:/media/control_center/set_setting_01.png')
        self.setting.add_flag(lv.obj.FLAG.CLICKABLE)
        self.setting.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.setting.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.setting_action),
            lv.EVENT.CLICKED,
            None
        )

        self.savepower_bg = lv.img(self)
        self.savepower_bg.set_src('E:/media/control_center/set_savepower_02.png')
        self.savepower_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 1, 1,
            lv.GRID_ALIGN.START, 1, 1
        )
        self.savepower = lv.img(self.savepower_bg)
        self.savepower.set_src('E:/media/control_center/set_savepower_01.png')
        self.savepower.add_flag(lv.obj.FLAG.CLICKABLE)
        self.savepower.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.savepower.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.savepower_action),
            lv.EVENT.CLICKED,
            None
        )

        self.dndm_bg = lv.img(self)
        self.dndm_bg.set_src('E:/media/control_center/set_dndm_02.png')
        self.dndm_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 2, 1,
            lv.GRID_ALIGN.START, 1, 1
        )
        self.dndm = lv.img(self.dndm_bg)
        self.dndm.set_src('E:/media/control_center/set_dndm_01.png')
        self.dndm.add_flag(lv.obj.FLAG.CLICKABLE)
        self.dndm.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.dndm.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.dndm_action),
            lv.EVENT.CLICKED,
            None
        )

        self.lock_bg = lv.img(self)
        self.lock_bg.set_src('E:/media/control_center/set_lock_02.png')
        self.lock_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 3, 1,
            lv.GRID_ALIGN.START, 1, 1
        )
        self.lock = lv.img(self.lock_bg)
        self.lock.set_src('E:/media/control_center/set_lock_01.png')
        self.lock.add_flag(lv.obj.FLAG.CLICKABLE)
        self.lock.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.lock.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.lock_action),
            lv.EVENT.CLICKED,
            None
        )

        self.info_bg = lv.img(self)
        self.info_bg.set_src('E:/media/control_center/set_info_02.png')
        self.info_bg.set_grid_cell(
            lv.GRID_ALIGN.START, 4, 1,
            lv.GRID_ALIGN.START, 1, 1
        )
        self.info = lv.img(self.info_bg)
        self.info.set_src('E:/media/control_center/set_info_01.png')
        self.info.add_flag(lv.obj.FLAG.CLICKABLE)
        self.info.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.info.add_event_cb(
            lambda event: self.__icon_click_cb(event, action=self.info_action),
            lv.EVENT.CLICKED,
            None
        )

    def __icon_click_cb(self, event, action=None):
        icon = event.get_target()
        if icon.get_style_opa(lv.PART.MAIN) == lv.OPA.COVER:
            icon.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
            action('off...')
        else:
            icon.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
            action('on...')

    def dndm_action(self, action):
        print('dndm_action: {}'.format(action))

    def flashlight_action(self, action):
        print('flashlight_action: {}'.format(action))

    def lift_action(self, action):
        print('lift_action: {}'.format(action))

    def findphone_action(self, action):
        print('findphone_action: {}'.format(action))

    def audio_action(self, action):
        print('audio_action: {}'.format(action))

    def savepower_action(self, action):
        print('savepower_action: {}'.format(action))

    def lock_action(self, action):
        print('lock_action: {}'.format(action))

    def info_action(self, action):
        print('info_action: {}'.format(action))

    def setting_action(self, action):
        print('setting_action: {}'.format(action))


class ControlCenterView(lv.obj):
    BATTERY_ICON = 'E:/media/control_center/set_batt_icon.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 320)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
        self.set_style_radius(0, lv.PART.MAIN)
        self.set_style_border_width(0, lv.PART.MAIN)
        self.remove_style(None, lv.PART.SCROLLBAR)

        self.battery = lv.img(self)
        self.battery.set_size(26, 14)
        self.battery.set_src(self.BATTERY_ICON)
        self.battery.set_offset_y(-14 * 9)

        self.time_label = lv.label(self)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.functions_view = FunctionsView(self)
        self.functions_view.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

    def enter(self):
        print('enter {}'.format(type(self).__name__))
        self.functions_view.scroll_to_x(0, lv.PART.MAIN)

    def exit(self):
        print('exit {}'.format(type(self).__name__))
