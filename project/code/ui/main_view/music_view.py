import sys_bus
import lvgl as lv
from ..language import tr
from ..font import Font


class MusicView(lv.canvas):
    MUSIC_PREV_ICON = 'E:/media/music/music_prev.png'
    MUSIC_NEXT_ICON = 'E:/media/music/music_next.png'
    MUSIC_MIDDLE_BG_ICON = 'E:/media/music/music_middle_bg.png'
    MUSIC_START_ICON = 'E:/media/music/music_start.png'
    MUSIC_VOLUME_ICON = 'E:/media/music/music_volume.png'
    MUSIC_VOLUME_UP_ICON = 'E:/media/music/music_volume_up.png'
    MUSIC_VOLUME_DOWN_ICON = 'E:/media/music/music_volume_down.png'

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.set_size(240, 320)
        self.set_layout(lv.LAYOUT_FLEX.value)
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.SPACE_EVENLY)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        self.music_label = lv.label(self)
        self.music_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.music_label.set_text(tr('Music'))

        self.time_label = lv.label(self)
        self.time_label.set_style_text_color(lv.color_white(), lv.PART.MAIN)
        self.time_label.set_text('{:02d}:{:02d}'.format(0, 0))

        self.prev_btn = lv.img(self)
        self.prev_btn.set_size(34, 30)
        self.prev_btn.set_src(self.MUSIC_PREV_ICON)
        self.prev_btn.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)

        self.ctrl_value = True
        self.ctrl_btn = lv.img(self)
        self.ctrl_btn.set_size(96, 96)
        self.ctrl_btn.set_src(self.MUSIC_MIDDLE_BG_ICON)

        self.next_btn = lv.img(self)
        self.next_btn.set_size(34, 30)
        self.next_btn.set_src(self.MUSIC_NEXT_ICON)

        self.volume_down = lv.img(self)
        self.volume_down.set_size(26, 25)
        self.volume_down.set_src(self.MUSIC_VOLUME_DOWN_ICON)
        self.volume_down.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK | lv.obj.FLAG.CLICKABLE)
        self.volume_down.add_event_cb(self.__volume_click_cb, lv.EVENT.CLICKED, None)

        self.volume_level = 0
        self.volume = lv.img(self)
        self.volume.set_size(160, 8)
        self.volume.set_src(self.MUSIC_VOLUME_ICON)

        self.volume_up = lv.img(self)
        self.volume_up.set_size(26, 25)
        self.volume_up.set_src(self.MUSIC_VOLUME_UP_ICON)
        self.volume_up.add_flag(lv.obj.FLAG.CLICKABLE)
        self.volume_up.add_event_cb(self.__volume_click_cb, lv.EVENT.CLICKED, None)

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_time(self, now):
        self.time_label.set_text('{:02d}:{:02d}'.format(now.hour, now.minute))

    def __volume_click_cb(self, event):
        icon = event.get_target()
        if icon is self.volume_up:
            self.volume_level += 1
            self.volume_level = self.volume_level if self.volume_level <= 10 else 10
        else:
            self.volume_level -= 1
            self.volume_level = self.volume_level if self.volume_level >= 0 else 0
        self.volume.set_offset_y(-8 * self.volume_level)
