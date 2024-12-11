"""主界面，表盘04"""
import sys_bus
import lvgl as lv
from usr.topics import UPDATE_DATETIME_TOPIC


class DateTimeView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/clk04/clk_hour.png'
    SEPARATOR_IMG_SRC = 'E:/media/clk04/clk_hour01.png'
    DATE_IMG_SRC = 'E:/media/clk04/clk_daydate.png'
    AM_PM_IMG_SRC = 'E:/media/clk04/clk_am.png'
    WEEKDAY_IMG_SRC = 'E:/media/clk04/clk_week_en.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(227, 93)
        self.set_pos(10, 19)

        self.hour_high = lv.img(self)
        self.hour_high.set_size(51, 67)
        self.hour_high.set_pos(0, 0)
        self.hour_high.set_src(self.DIGIT_IMG_SRC)
        self.hour_high.set_offset_y(0)

        self.hour_low = lv.img(self)
        self.hour_low.set_size(51, 67)
        self.hour_low.set_pos(52, 0)
        self.hour_low.set_src(self.DIGIT_IMG_SRC)
        self.hour_low.set_offset_y(0)

        self.time_separator = lv.img(self)
        self.time_separator.set_size(13, 35)
        self.time_separator.set_pos(107, 16)
        self.time_separator.set_src(self.SEPARATOR_IMG_SRC)

        self.minute_high = lv.img(self)
        self.minute_high.set_size(51, 67)
        self.minute_high.set_pos(124, 0)
        self.minute_high.set_src(self.DIGIT_IMG_SRC)
        self.minute_high.set_offset_y(0)

        self.minute_low = lv.img(self)
        self.minute_low.set_size(51, 67)
        self.minute_low.set_pos(172, 0)
        self.minute_low.set_src(self.DIGIT_IMG_SRC)
        self.minute_low.set_offset_y(0)

        self.month_high = lv.img(self)
        self.month_high.set_src(self.DATE_IMG_SRC)
        self.month_high.set_size(12, 17)
        self.month_high.set_pos(17, 76)

        self.month_low = lv.img(self)
        self.month_low.set_src(self.DATE_IMG_SRC)
        self.month_low.set_size(12, 17)
        self.month_low.set_pos(30, 76)

        self.date_separator = lv.img(self)
        self.date_separator.set_src(self.DATE_IMG_SRC)
        self.date_separator.set_size(12, 17)
        self.date_separator.set_pos(43, 76)
        self.date_separator.set_offset_y(-170)

        self.day_high = lv.img(self)
        self.day_high.set_src(self.DATE_IMG_SRC)
        self.day_high.set_size(12, 17)
        self.day_high.set_pos(56, 76)

        self.day_low = lv.img(self)
        self.day_low.set_size(12, 17)
        self.day_low.set_src(self.DATE_IMG_SRC)
        self.day_low.set_pos(69, 76)

        self.am_pm = lv.img(self)
        self.am_pm.set_src(self.AM_PM_IMG_SRC)
        self.am_pm.set_size(28, 34)
        self.am_pm.set_pos(97, 76)

        self.weekday = lv.img(self)
        self.weekday.set_src(self.WEEKDAY_IMG_SRC)
        self.weekday.set_size(46, 21)
        self.weekday.set_pos(170, 76)
        self.weekday.set_offset_y(-3)

    def update(self, month, day, hour, minute, weekday):
        # 12小时制
        hour_string = '{:02d}'.format(hour if hour <= 12 else hour % 12)
        minute_string = '{:02d}'.format(minute)
        month_string = '{:02d}'.format(month)
        day_string = '{:02d}'.format(day)
        self.hour_high.set_offset_y(-67 * int(hour_string[0]))
        self.hour_low.set_offset_y(-67 * int(hour_string[1]))
        self.minute_high.set_offset_y(-67 * int(minute_string[0]))
        self.minute_low.set_offset_y(-67 * int(minute_string[1]))
        self.am_pm.set_offset_y(-17 if hour >= 12 else 0)
        self.month_high.set_offset_y(-17 * int(month_string[0]))
        self.month_low.set_offset_y(-17 * int(month_string[1]))
        self.day_high.set_offset_y(-17 * int(day_string[0]))
        self.day_low.set_offset_y(-17 * int(day_string[1]))
        self.weekday.set_offset_y(-3 - (21 * (6 if weekday == 0 else weekday - 1)))
        self.blink()

    def blink(self):
        if self.time_separator.is_visible():
            self.time_separator.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.time_separator.clear_flag(lv.obj.FLAG.HIDDEN)


class StepGraphView(lv.canvas):
    BG_IMG_SRC = 'E:/media/clk04/clk04_bg_01.png'
    GOAL_IMG_SRC = 'E:/media/clk04/Goal.png'
    GOAL_DIGIT_IMG_SRC = 'E:/media/clk04/clk_daydate.png'
    TOTAL_DIGIT_IMG_SRC = 'E:/media/clk04/clk_step.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(229, 84)
        self.set_pos(0, 0)

        self.bg = lv.img(self)
        self.bg.set_src(self.BG_IMG_SRC)
        self.bg.set_size(229, 84)
        self.bg.set_pos(0, 0)

        self.goal = lv.img(self)
        self.goal.set_src(self.GOAL_IMG_SRC)
        self.goal.set_size(44, 17)
        self.goal.set_pos(8, 13)

        # goal step
        self.goal_step_digit_list = []
        for i in range(5):
            img = lv.img(self)
            img.set_src(self.GOAL_DIGIT_IMG_SRC)
            img.set_size(12, 17)
            img.set_pos(8+44+4+(i*12), 13)
            img.set_offset_y(0)
            self.goal_step_digit_list.append(img)

        # total step
        self.total_step_digit_list = []
        for i in range(5):
            img = lv.img(self)
            img.set_src(self.TOTAL_DIGIT_IMG_SRC)
            img.set_size(20, 29)
            img.set_pos(8+(i*20), 13+17+15)
            img.set_offset_y(0)
            self.total_step_digit_list.append(img)

    def update(self, value, goal=None):
        value_string = '{:05d}'.format(value)
        for index, img in enumerate(self.total_step_digit_list):
            img.set_offset_y(-29 * int(value_string[index]))
        if goal is not None:
            goal_string = '{:05d}'.format(goal)
            for index, img in enumerate(self.goal_step_digit_list):
                img.set_offset_y(-17 * int(goal_string[index]))


class HrGraphView(lv.canvas):
    BG_IMG_SRC = 'E:/media/clk04/clk04_bg_02.png'
    DIGIT1_IMG_SRC = 'E:/media/clk04/clk_daydate.png'
    DIGIT2_IMG_SRC = 'E:/media/clk04/clk_step.png'
    HR_UNIT_IMG_SRC = 'E:/media/clk04/clk_bpm.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(229, 84)
        self.set_pos(0, 0)

        self.bg = lv.img(self)
        self.bg.set_src(self.BG_IMG_SRC)
        self.bg.set_size(229, 84)
        self.bg.set_pos(0, 0)

        self.top_hr_digit_list = []
        for i in range(3):
            img = lv.img(self)
            img.set_src(self.DIGIT1_IMG_SRC)
            img.set_size(12, 17)
            img.set_pos(30+(i*12), 14-4)
            img.set_offset_y(0)
            self.top_hr_digit_list.append(img)

        self.bottom_hr_digit_list = []
        for i in range(3):
            img = lv.img(self)
            img.set_src(self.DIGIT1_IMG_SRC)
            img.set_size(12, 17)
            img.set_pos(97+(i*12), 14-4)
            img.set_offset_y(0)
            self.bottom_hr_digit_list.append(img)

        self.hr_digit_list = []
        for i in range(3):
            img = lv.img(self)
            img.set_src(self.DIGIT2_IMG_SRC)
            img.set_size(20, 29)
            img.set_pos(12+(i*20), 45)
            img.set_offset_y(0)
            self.hr_digit_list.append(img)

        self.hr_unit = lv.img(self)
        self.hr_unit.set_src(self.HR_UNIT_IMG_SRC)
        self.hr_unit.set_size(41, 18)
        self.hr_unit.set_pos(72+4, 56)

    def update(self, hr, top_hr=None, bottom_hr=None):
        hr_string = '{:03d}'.format(hr)
        for index, img in enumerate(self.hr_digit_list):
            img.set_offset_y(-29 * int(hr_string[index]))

        if top_hr is not None:
            top_hr_string = '{:03d}'.format(top_hr)
            for index, img in enumerate(self.top_hr_digit_list):
                img.set_offset_y(-17 * int(top_hr_string[index]))

        if bottom_hr is not None:
            bottom_hr_string = '{:03d}'.format(bottom_hr)
            for index, img in enumerate(self.bottom_hr_digit_list):
                img.set_offset_y(-17 * int(bottom_hr_string[index]))


class KcalGraphView(lv.canvas):
    BG_IMG_SRC = 'E:/media/clk04/clk04_bg_03.png'
    GOAL_IMG_SRC = 'E:/media/clk04/Goal.png'
    GOAL_DIGIT_IMG_SRC = 'E:/media/clk04/clk_daydate.png'
    TOTAL_DIGIT_IMG_SRC = 'E:/media/clk04/clk_step.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(229, 84)
        self.set_pos(0, 0)

        self.bg = lv.img(self)
        self.bg.set_src(self.BG_IMG_SRC)
        self.bg.set_size(229, 84)
        self.bg.set_pos(0, 0)

        self.goal = lv.img(self)
        self.goal.set_src(self.GOAL_IMG_SRC)
        self.goal.set_size(44, 17)
        self.goal.set_pos(8, 13)

        # goal kcal
        self.goal_kcal_digit_list = []
        for i in range(4):
            img = lv.img(self)
            img.set_src(self.GOAL_DIGIT_IMG_SRC)
            img.set_size(12, 17)
            img.set_pos(8 + 44 + 4 + (i * 12), 13)
            img.set_offset_y(0)
            self.goal_kcal_digit_list.append(img)

        # total kcal
        self.total_kcal_digit_list = []
        for i in range(4):
            img = lv.img(self)
            img.set_src(self.TOTAL_DIGIT_IMG_SRC)
            img.set_size(20, 29)
            img.set_pos(8 + (i * 20), 13 + 17 + 15)
            img.set_offset_y(0)
            self.total_kcal_digit_list.append(img)

    def update(self, value, goal=None):
        value_string = '{:04d}'.format(value)
        for index, img in enumerate(self.total_kcal_digit_list):
            img.set_offset_y(-29 * int(value_string[index]))
        if goal is not None:
            goal_string = '{:04d}'.format(goal)
            for index, img in enumerate(self.goal_kcal_digit_list):
                img.set_offset_y(-17 * int(goal_string[index]))


class GraphView(lv.canvas):
    STEP_ICON_IMG_SRC = 'E:/media/clk04/clk04_iocn_01.png'
    HR_ICON_IMG_SRC = 'E:/media/clk04/clk04_iocn_02.png'
    KCAL_ICON_IMG_SRC = 'E:/media/clk04/clk04_iocn_03.png'
    ALL_ICON_IMG_SRC = 'E:/media/clk04/clk04_iocn_04.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(229, 50+94)
        self.set_pos(5, 122)

        self.step_graph = StepGraphView(self)
        self.step_graph.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        self.hr_graph = HrGraphView(self)

        self.kcal_graph = KcalGraphView(self)
        self.kcal_graph.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        self.all_icon = lv.img(self)
        self.all_icon.set_src(self.ALL_ICON_IMG_SRC)
        self.all_icon.set_size(220, 50)
        self.all_icon.set_pos(0, 94)

        self.step_icon = lv.img(self.all_icon)
        self.step_icon.set_src(self.STEP_ICON_IMG_SRC)
        self.step_icon.set_size(50, 50)
        self.step_icon.set_pos(0, 0)
        self.step_icon.add_flag(lv.obj.FLAG.CLICKABLE)
        self.step_icon.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.step_icon.add_event_cb(
            lambda event: self.__icon_click_cb(event, graph=self.step_graph),
            lv.EVENT.CLICKED,
            None
        )

        self.hr_icon = lv.img(self.all_icon)
        self.hr_icon.set_src(self.HR_ICON_IMG_SRC)
        self.hr_icon.set_size(50, 50)
        self.hr_icon.set_pos(85, 0)
        self.hr_icon.add_flag(lv.obj.FLAG.CLICKABLE)
        self.hr_icon.add_event_cb(
            lambda event: self.__icon_click_cb(event, graph=self.hr_graph),
            lv.EVENT.CLICKED,
            None
        )

        self.kcal_icon = lv.img(self.all_icon)
        self.kcal_icon.set_src(self.KCAL_ICON_IMG_SRC)
        self.kcal_icon.set_size(50, 50)
        self.kcal_icon.set_pos(170, 0)
        self.kcal_icon.add_flag(lv.obj.FLAG.CLICKABLE)
        self.kcal_icon.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.kcal_icon.add_event_cb(
            lambda event: self.__icon_click_cb(event, graph=self.kcal_graph),
            lv.EVENT.CLICKED,
            None
        )

    def __icon_click_cb(self, event, graph=None):
        icon = event.get_target()
        if icon.get_style_opa(lv.PART.MAIN) == lv.OPA.COVER:
            return

        targets = [self.step_icon, self.hr_icon, self.kcal_icon]
        targets.remove(icon)
        for t in targets:
            t.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        graphs = [self.step_graph, self.hr_graph, self.kcal_graph]
        graphs.remove(graph)
        for g in graphs:
            g.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)

        icon.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
        graph.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)


class Clk04View(lv.canvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 320)
        self.set_style_bg_opa(lv.OPA.COVER, lv.PART.MAIN)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        self.date_time = DateTimeView(self)
        self.graph = GraphView(self)

        self.update_kcal({'value': 2500, 'goal': 5000})
        self.update_step({'value': 12345, 'goal': 50000})
        self.update_heart_rate({'value': 95, 'top': 97, 'bottom': 85})

        sys_bus.subscribe(UPDATE_DATETIME_TOPIC, lambda topic, now: self.update_datetime(now))

    def enter(self):
        print('enter {}'.format(type(self).__name__))

    def exit(self):
        print('exit {}'.format(type(self).__name__))

    def update_datetime(self, now):
        self.date_time.update(now.month, now.day, now.hour, now.minute, now.weekday)
        # self.date_time.blink()

    def update_kcal(self, data):
        self.graph.kcal_graph.update(
            data['value'],
            goal=data.get('goal', None)
        )

    def update_step(self, data):
        self.graph.step_graph.update(
            data['value'],
            goal=data.get('goal', None)
        )

    def update_heart_rate(self, data):
        self.graph.hr_graph.update(
            data['value'],
            top_hr=data.get('top', None),
            bottom_hr=data.get('bottom', None)
        )
