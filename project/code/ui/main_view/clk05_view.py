"""主界面，表盘05"""
import lvgl as lv
import sys_bus


class ClockView(lv.canvas):
    HOUR_HAND_SRC = 'E:/media/clk05/clk05_hour.png'
    MINUTE_HAND_SRC = 'E:/media/clk05/clk05_min.png'
    SECOND_HAND_SRC = 'E:/media/clk05/clk05_second.png'
    POINT_SRC = 'E:/media/clk05/clk05_hour_icon.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.set_pos(0, 0)

        # 时针
        self.hour_hand = lv.img(self)
        self.hour_hand.set_src(self.HOUR_HAND_SRC)
        self.hour_hand.set_pos(72+79, 35+14)
        self.hour_hand.set_pivot(5, 44)
        self.hour_hand.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
        # 分针
        self.minute_hand = lv.img(self)
        self.minute_hand.set_src(self.MINUTE_HAND_SRC)
        self.minute_hand.set_pos(72+79, 5+14)
        self.minute_hand.set_pivot(5, 74)
        self.minute_hand.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
        # 秒针
        self.second_hand = lv.img(self)
        self.second_hand.set_src(self.SECOND_HAND_SRC)
        self.second_hand.set_pos(74+79, 5+14)
        self.second_hand.set_pivot(3, 72)
        self.second_hand.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)
        # 原点
        self.point = lv.img(self)
        self.point.set_src(self.POINT_SRC)
        self.point.set_pos(72+79, 72+14)
        self.point.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)

    def update(self, hour, minute, second):
        angle_for_second = second * 6  # 秒度
        self.second_hand.set_angle(angle_for_second * 10)
        angle_for_minute = minute * 6 + angle_for_second / 60  # 分度
        self.minute_hand.set_angle(int(angle_for_minute * 10))
        angle_for_hour = hour * 30 + angle_for_minute / 12  # 时度
        self.hour_hand.set_angle(int(angle_for_hour * 10))


class KcalView(lv.canvas):
    KCAL_UNIT = 1 / 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(66, 65)
        self.set_pos(9, 17)

        self.kcal_arc = lv.arc(self)
        self.kcal_arc.set_size(66, 65)
        self.kcal_arc.remove_style(None, lv.PART.KNOB)
        self.kcal_arc.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.kcal_arc.set_style_arc_width(6, lv.PART.INDICATOR)
        self.kcal_arc.set_style_arc_color(lv.color_hex(0xFFAE00), lv.PART.INDICATOR)
        self.kcal_arc.set_style_arc_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.kcal_arc.set_value(0)

        self.kcal_label = lv.label(self.kcal_arc)
        self.kcal_label.set_style_text_color(lv.color_hex(0xFFF000), lv.PART.MAIN)
        self.kcal_label.set_text(str(0))
        self.kcal_label.center()

    def update(self, value):
        self.kcal_label.set_text(str(value))
        self.kcal_arc.set_value(int(value * self.KCAL_UNIT))


class StepView(lv.canvas):
    STEP_UNIT = 1 / 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(66, 65)
        self.set_pos(9, 99)

        self.step_arc = lv.arc(self)
        self.step_arc.set_size(66, 65)
        self.step_arc.remove_style(None, lv.PART.KNOB)
        self.step_arc.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.step_arc.set_style_arc_width(6, lv.PART.INDICATOR)
        self.step_arc.set_style_arc_color(lv.color_hex(0x9FFC0C), lv.PART.INDICATOR)
        self.step_arc.set_style_arc_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.step_arc.set_value(0)

        self.step_label = lv.label(self.step_arc)
        self.step_label.set_style_text_color(lv.color_hex(0x00FF42), lv.PART.MAIN)
        self.step_label.set_text(str(0))
        self.step_label.center()

    def update(self, value):
        self.step_label.set_text(str(value))
        self.step_arc.set_value(int(value * self.STEP_UNIT))


class DigitTimeView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/clk05/clk05_hour01.png'
    SEPARATOR_IMG_SRC = 'E:/media/clk05/clk05_hour02.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(179, 54)
        self.set_pos(31, 206)

        # hour
        self.hour_high = lv.img(self)
        self.hour_high.set_size(41, 54)
        self.hour_high.set_pos(0, 0)
        self.hour_high.set_src(self.DIGIT_IMG_SRC)
        self.hour_high.set_offset_y(0)

        self.hour_low = lv.img(self)
        self.hour_low.set_size(41, 54)
        self.hour_low.set_pos(41, 0)
        self.hour_low.set_src(self.DIGIT_IMG_SRC)
        self.hour_low.set_offset_y(0)

        # separator
        self.separator = lv.img(self)
        self.separator.set_size(11, 35)
        self.separator.set_pos(84, 12)
        self.separator.set_src(self.SEPARATOR_IMG_SRC)

        # minute
        self.minute_high = lv.img(self)
        self.minute_high.set_size(41, 54)
        self.minute_high.set_pos(97, 0)
        self.minute_high.set_src(self.DIGIT_IMG_SRC)
        self.minute_high.set_offset_y(0)

        self.minute_low = lv.img(self)
        self.minute_low.set_size(41, 54)
        self.minute_low.set_pos(138, 0)
        self.minute_low.set_src(self.DIGIT_IMG_SRC)
        self.minute_low.set_offset_y(0)

    def update(self, hour, minute):
        hour_string = '{:02d}'.format(hour)
        minute_string = '{:02d}'.format(minute)
        self.hour_high.set_offset_y(-54 * int(hour_string[0]))
        self.hour_low.set_offset_y(-54 * int(hour_string[1]))
        self.minute_high.set_offset_y(-54 * int(minute_string[0]))
        self.minute_low.set_offset_y(-54 * int(minute_string[1]))

    def blink(self):
        if self.separator.is_visible():
            self.separator.add_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.separator.clear_flag(lv.obj.FLAG.HIDDEN)


class DayDateView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/clk05/clk_daydate.png'
    WEEKDAY_IMG_SRC = 'E:/media/clk05/clk_week_en.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(121, 17)
        self.set_pos(10, 170)

        # month
        self.month_high = lv.img(self)
        self.month_high.set_size(12, 17)
        self.month_high.set_pos(0, 0)
        self.month_high.set_src(self.DIGIT_IMG_SRC)
        self.month_high.set_offset_y(0)

        self.month_low = lv.img(self)
        self.month_low.set_size(12, 17)
        self.month_low.set_pos(13, 0)
        self.month_low.set_src(self.DIGIT_IMG_SRC)
        self.month_low.set_offset_y(0)

        # separator
        self.separator = lv.img(self)
        self.separator.set_size(12, 17)
        self.separator.set_pos(26, 0)
        self.separator.set_src(self.DIGIT_IMG_SRC)
        self.separator.set_offset_y(-170)

        # day
        self.day_high = lv.img(self)
        self.day_high.set_size(12, 17)
        self.day_high.set_pos(39, 0)
        self.day_high.set_src(self.DIGIT_IMG_SRC)
        self.day_high.set_offset_y(0)

        self.day_low = lv.img(self)
        self.day_low.set_size(12, 17)
        self.day_low.set_pos(52, 0)
        self.day_low.set_src(self.DIGIT_IMG_SRC)
        self.day_low.set_offset_y(0)

        # weekday
        self.weekday = lv.img(self)
        self.weekday.set_size(46, 17)
        self.weekday.set_pos(78, 0)
        self.weekday.set_src(self.WEEKDAY_IMG_SRC)
        self.weekday.set_offset_y(-3)

    def update(self, month, day, weekday):
        month_string = '{:02d}'.format(month)
        day_string = '{:02d}'.format(day)
        self.month_high.set_offset_y(-17 * int(month_string[0]))
        self.month_low.set_offset_y(-17 * int(month_string[1]))
        self.day_high.set_offset_y(-17 * int(day_string[0]))
        self.day_low.set_offset_y(-17 * int(day_string[1]))
        self.weekday.set_offset_y(-3 - (21 * (6 if weekday == 0 else weekday - 1)))


class BatteryView(lv.canvas):
    ICON_IMG_SRC = 'E:/media/clk05/clk05_bat_icon01.png'
    GRAPH_IMG_SRC = 'E:/media/clk05/clk05_bat0.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(15, 63)
        self.set_pos(10, 191)

        self.icon = lv.img(self)
        self.icon.set_size(12, 24)
        self.icon.set_pos(0, 0)
        self.icon.set_src(self.ICON_IMG_SRC)
        self.icon.set_offset_y(0)

        self.graph = lv.img(self)
        self.graph.set_size(15, 34)
        self.graph.set_pos(0, 39)
        self.graph.set_src(self.GRAPH_IMG_SRC)
        self.graph.set_offset_y(0)

    def update(self, level):
        """level(0~9)"""
        self.icon.set_offset_y(-24 * level)
        self.graph.set_offset_y(-34 * level)


class HeartRateView(lv.canvas):
    DIGIT_IMG_SRC = 'E:/media/clk05/clk05_hr01.png'
    GRAPH_IMG_SRC = 'E:/media/clk05/clk05_hr02.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(25, 79)
        self.set_pos(209, 175)

        # 百分位
        self.hundredth = lv.img(self)
        self.hundredth.set_src(self.DIGIT_IMG_SRC)
        self.hundredth.set_size(8, 12)
        self.hundredth.set_pos(0, 0)
        self.hundredth.set_offset_y(0)

        # 十分位
        self.tenth = lv.img(self)
        self.tenth.set_src(self.DIGIT_IMG_SRC)
        self.tenth.set_size(8, 12)
        self.tenth.set_pos(9, 0)
        self.tenth.set_offset_y(0)

        # 个位
        self.oneth = lv.img(self)
        self.oneth.set_src(self.DIGIT_IMG_SRC)
        self.oneth.set_size(8, 12)
        self.oneth.set_pos(18, 0)
        self.oneth.set_offset_y(0)

        # 图表
        self.graph = lv.img(self)
        self.graph.set_src(self.GRAPH_IMG_SRC)
        self.graph.set_size(15, 39)
        self.graph.set_pos(4, 40)
        self.graph.set_offset_y(0)

    def update(self, value):
        # 成人正常心率为60～100次/分钟，理想心率应为55～70次/分钟
        value_string = '{:03d}'.format(value)
        self.hundredth.set_offset_y(-12 * int(value_string[0]))
        self.tenth.set_offset_y(-12 * int(value_string[1]))
        self.oneth.set_offset_y(-12 * int(value_string[2]))

        # TODO: 心率级别如何划分？
        if value <= 0:  # 无心率数值
            self.graph.set_offset_y(-39 * 0)
        elif value <= 55:  # 心率偏低
            self.graph.set_offset_y(-39 * 1)
        elif value <= 70:  # 理想心率
            self.graph.set_offset_y(-39 * 6)
        elif value <= 100:  # 正常心率
            self.graph.set_offset_y(-39 * 5)
        elif value <= 110:  # 心率偏高
            self.graph.set_offset_y(-39 * 4)
        elif value <= 120:  # 心率超高
            self.graph.set_offset_y(-39 * 3)
        else:  # 危险！！！
            self.graph.set_offset_y(-39 * 2)


class Clk05View(lv.canvas):
    BG_IMG_SRC = 'E:/media/clk05/clk05_bg.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 320)
        self.set_style_bg_color(lv.color_black(), lv.PART.MAIN)

        # background image
        self.bg = lv.img(self)
        self.bg.set_src(self.BG_IMG_SRC)
        self.bg.set_size(240, 280)

        # clock
        self.clock = ClockView(self)

        # kcal
        self.kcal = KcalView(self)

        # step
        self.step = StepView(self)

        # digit time area
        self.digit_time = DigitTimeView(self)

        # day date area
        self.day_date = DayDateView(self)

        # battery area
        self.battery = BatteryView(self)

        # heart rate area
        self.heart_rate = HeartRateView(self)

    def update_datetime(self, now):
        self.clock.update(now.hour, now.minute, now.second)
        self.digit_time.update(now.hour, now.minute)
        self.digit_time.blink()
        self.day_date.update(now.month, now.day, now.weekday)

    def update_battery(self, level):
        # level: 0~9
        self.battery.update(level)

    def update_kcal(self, data):
        self.kcal.update(data['value'])

    def update_step(self, data):
        self.step.update(data['value'])

    def update_heart_rate(self, data):
        self.heart_rate.update(data['value'])
