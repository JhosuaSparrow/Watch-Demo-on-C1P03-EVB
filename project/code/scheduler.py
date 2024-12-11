import lvgl as lv
import sys_bus
import voiceCall
from usr.qframe.datetime import DateTime
from usr.topics import UPDATE_DATETIME_TOPIC
from usr.topics import LOAD_INCOMING_CALL_VIEW, FUNC_VOLTE_CONNECTED, LOAD_MAIN_VIEW


def voicecallFun(args):
    print('args: ', args)
    if args[0] == 10:
        print('来电通知，响铃（volte通话）, ', args)
        sys_bus.publish(LOAD_INCOMING_CALL_VIEW, {'phone_number': args[6]})
    elif args[0] == 11:
        print('通话接通（volte通话）: ', args)
        sys_bus.publish(FUNC_VOLTE_CONNECTED, {})
    elif args[0] == 12:
        print('通话挂断（volte通话）: ', args)
        sys_bus.publish(LOAD_MAIN_VIEW, {})
    elif args[0] == 13:
        print('呼叫等待（volte通话）: ', args)
    elif args[0] == 14:
        print('呼出中（volte通话）: ', args)
    elif args[0] == 15:
        print('呼出中，对方未响铃（volte通话）: ', args)
    elif args[0] == 16:
        print('等待（volte通话）: ', args)
    else:
        return


def update_datetime(timer):
    now = DateTime.now()
    sys_bus.publish_sync(UPDATE_DATETIME_TOPIC, now)


def test_scheduler():
    voiceCall.setCallback(voicecallFun)
    time_updater = lv.timer_create(update_datetime, 1000, None)


if __name__ == '__main__':
    test_scheduler()
