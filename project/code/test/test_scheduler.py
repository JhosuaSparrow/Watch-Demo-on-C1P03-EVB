import sys_bus
import urandom as random
import lvgl as lv
import utime
from usr.qframe.datetime import DateTime
from usr.qframe.scheduler import Scheduler
from usr.qframe.threading import Thread
from usr.topic import *

scheduler = Scheduler()


@scheduler.task(UPDATE_BATTERY_TOPIC, interval=30)
def update_battery():
    sys_bus.publish_sync(UPDATE_BATTERY_TOPIC, random.randint(0, 9))


@scheduler.task(UPDATE_STEP_TOPIC, interval=40)
def update_step():
    sys_bus.publish_sync(
        UPDATE_STEP_TOPIC,
        {
            'value': random.randint(10000, 30000),
            'goal': 50000
        }
    )


@scheduler.task(UPDATE_HEART_RATE_TOPIC, interval=50)
def update_heart_rate():
    sys_bus.publish_sync(
        UPDATE_HEART_RATE_TOPIC,
        {
            'value': random.randint(0, 120),
            'top': 120,
            'bottom': 15
        }
    )


@scheduler.task(UPDATE_KCAL_TOPIC, interval=60)
def update_kcal():
    sys_bus.publish_sync(
        UPDATE_KCAL_TOPIC,
        {
            'value': random.randint(1000, 2000),
            'goal': 3000
        }
    )


@scheduler.task(UPDATE_SLEEP_TIME_TOPIC, interval=30)
def update_sleep_time():
    sys_bus.publish_sync(
        UPDATE_SLEEP_TIME_TOPIC,
        {
            'hour': random.randint(0, 12),
            'minute': 30
        }
    )


@scheduler.task(UPDATE_RECENT_SLEEP_TIME_TOPIC, interval=30)
def update_recent_sleep_time():
    sys_bus.publish_sync(
        UPDATE_RECENT_SLEEP_TIME_TOPIC,
        [60*8,60*5+45,60*3+15,60*8+15,60*10,60*5,60*3+90]
    )


@scheduler.task(UPDATE_UV_INDEX_TOPIC, interval=30)
def update_uv_index():
    sys_bus.publish_sync(
        UPDATE_UV_INDEX_TOPIC,
        random.randint(0, 14)
    )


def update_datetime(timer):
    now = DateTime.now()
    sys_bus.publish_sync(UPDATE_DATETIME_TOPIC, now)


def test_update_spo2_data():
    data = []
    for i in range(31):
        value = random.randint(0, 100)
        data.append(value)
        sys_bus.publish_sync(UPDATE_SPO2_TOPIC, value)
        sys_bus.publish_sync(UPDATE_SPO2_REMAINING_TOPIC, {'value': 30-i, 'hidden': False})
        utime.sleep(1)
    sys_bus.publish_sync(UPDATE_SPO2_REMAINING_TOPIC, {'value': 0, 'hidden': True})
    sys_bus.publish_sync(UPDATE_SPO2_HIGHEST_AND_LOWEST_TOPIC, {'highest_value': max(data), 'lowest_value': min(data)})


def start_all_test_scheduler():
    time_updater = lv.timer_create(update_datetime, 1000, None)
    # scheduler.start()
    # Thread(target=test_update_spo2_data).start()


if __name__ == '__main__':
    start_all_test_scheduler()
