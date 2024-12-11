import sys_bus
import lvgl as lv
from usr.qframe.collections import Singleton
from .activity_view import ActivityView
from .sleep_view import SleepView
from .spo2_view import SpO2View
from .heart_rate_view import HeartRateView
from .pressure_view import PressureView
from .blood_pressure_view import BloodPressureView
from .uv_view import UVView
from .music_view import MusicView
from .clk05_view import Clk05View
from .clk04_view import Clk04View
from .control_center_view import ControlCenterView
from .message_list_view import MessageListView
from usr.topics import LOAD_MAIN_VIEW


@Singleton
class MainView(lv.tileview):
    view_name_to_info = {}
    tile_id_to_view_name = {}
    active_view = None

    def __init__(self):
        super().__init__(None)
        self.set_size(240, 320)
        self.remove_style(None, lv.PART.SCROLLBAR)

        self.insert_view('music_view',  MusicView, (0, 1), lv.DIR.RIGHT)
        self.insert_view('primary_view', Clk04View, (1, 1), lv.DIR.ALL)
        self.insert_view('activity_view', ActivityView, (2, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('sleep_view', SleepView, (3, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('spo2_view', SpO2View, (4, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('heart_rate_view', HeartRateView, (5, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('pressure_view', PressureView, (6, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('blood_pressure_view', BloodPressureView, (7, 1), lv.DIR.LEFT | lv.DIR.RIGHT)
        self.insert_view('uv_view', UVView, (8, 1), lv.DIR.LEFT)
        self.insert_view('control_center_view', ControlCenterView, (1, 0), lv.DIR.BOTTOM)
        self.insert_view('message_list_view', MessageListView, (1, 2), lv.DIR.TOP)

        self.add_event_cb(self.loaded_cb, 39, None)  # LV_EVENT_SCREEN_LOADED
        self.add_event_cb(self.unloaded_cb, 40, None)  # LV_EVENT_SCREEN_UNLOADED
        self.add_event_cb(self.__value_changed_cb, lv.EVENT.VALUE_CHANGED, None)

    def goto_view(self, view_name, anim=lv.ANIM.OFF):
        self.set_tile(self.get_info_by_view_name(view_name)['tile'], anim)

    def goto_primary(self):
        self.goto_view('primary_view')

    def loaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_LOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def unloaded_cb(self, event):
        print('{}({}) LV_EVENT_SCREEN_UNLOADED({})'.format(type(self).__name__, id(self), event.get_code()))

    def insert_view(self, view_name, view_class, pos, direction):
        tile = self.add_tile(pos[0], pos[1], direction)
        self.view_name_to_info[view_name] = {'tile': tile, 'pos': pos, 'view': view_class(tile)}
        self.tile_id_to_view_name[tile.get_child_id()] = view_name

    def get_info_by_view_name(self, view_name):
        return self.view_name_to_info[view_name]

    def get_info_by_tile_id(self, tile_id):
        return self.view_name_to_info[self.get_view_name_by_tile_id(tile_id)]

    def get_view_name_by_tile_id(self, tile_id):
        return self.tile_id_to_view_name[tile_id]

    def __value_changed_cb(self, event):
        tid = self.get_tile_act().get_child_id()
        print('{} LV_EVENT_VALUE_CHANGED({}), tile id: {}'.format(type(self).__name__, event.get_code(), tid))
        temp_view = self.get_info_by_tile_id(tid)['view']
        if self.active_view is temp_view:
            return
        getattr(self.active_view, 'exit', lambda: None)()
        self.active_view = temp_view
        getattr(self.active_view, 'enter', lambda: None)()


def load_main_view_cb(**kwargs):
    view_name = kwargs.get('view_name', None)
    mv = MainView()
    if view_name is not None:
        mv.goto_view(view_name)
    lv.scr_load(mv)


sys_bus.subscribe(LOAD_MAIN_VIEW, lambda topic, kwargs: load_main_view_cb(**kwargs))
