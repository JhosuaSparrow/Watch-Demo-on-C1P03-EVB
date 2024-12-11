import sys_bus
import ql_fs
from usr.qframe import CurrentApp
from usr.qframe.scheduler import Scheduler, Task, CronTrigger
from usr.qframe.logging import getLogger
from usr.topics import FUNC_ALARM_CLOCK_RUNNING

logger = getLogger(__name__)


class AlarmClock(Task):

    def __init__(self, hour, minute, weekdays=(), ring=True, shake=True, valid=True, title='N/A'):
        self.weekdays = weekdays or tuple(range(0, 7))
        self.ring = ring
        self.shake = shake
        self.valid = valid
        super().__init__(
            title=title,
            target=self.run,
            sync=True,
            trigger=CronTrigger(hour=hour, minute=minute)
        )

    @property
    def hour(self):
        return self.trigger.hour

    @property
    def minute(self):
        return self.trigger.minute

    def __str__(self):
        return '{}(title={}, hour={}, minute={}, weekdays={}, ring={}, shake={}, valid={})'.format(
            type(self).__name__,
            repr(self.title),
            self.hour,
            self.minute,
            self.weekdays,
            self.ring,
            self.shake,
            self.valid
        )

    def run(self):
        sys_bus.publish(FUNC_ALARM_CLOCK_RUNNING, self)
        logger.debug('{} run...'.format(self))


class AlarmListFullError(Exception):
    pass


class AlarmService(object):
    ALARM_DB_FILE_PATH = '/usr/alarm_info.json'
    MAX_ALARM_NUMBER = 24

    def __init__(self, app=None):
        self.alarms = []
        self.scheduler = Scheduler()
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.register('alarm_service', self)

    def load(self):
        logger.info('loading {}'.format(type(self).__name__))
        if ql_fs.path_exists(self.ALARM_DB_FILE_PATH):
            alarms_info = ql_fs.read_json(self.ALARM_DB_FILE_PATH)['alarms']
            for info in alarms_info:
                self.submit(**info)
        self.scheduler.start()

    def submit(self, hour, minute, weekdays=(), ring=True, shake=True, valid=True, title='N/A'):
        """submit a new alarm, and schedule it immediately"""
        if len(self.alarms) >= self.MAX_ALARM_NUMBER:
            raise AlarmListFullError
        alarm = AlarmClock(hour, minute, weekdays=weekdays, ring=ring, shake=shake, valid=valid, title=title)
        self.alarms.append(alarm)
        self.scheduler.add(alarm)
        return alarm

    def delete(self, alarm):
        """cancel a alarm"""
        self.scheduler.cancel(alarm)
        if alarm in self.alarms:
            self.alarms.remove(alarm)

    def update(self, alarm, **kwargs):
        """update a alarm"""
        hour = kwargs.get('hour', alarm.trigger.hour)
        minute = kwargs.get('minute', alarm.trigger.minute)
        alarm.weekdays = kwargs.get('weekdays', alarm.weekdays)
        alarm.ring = kwargs.get('ring', alarm.ring)
        alarm.shake = kwargs.get('shake', alarm.shake)
        alarm.valid = kwargs.get('valid', alarm.valid)
        alarm.title = kwargs.get('title', alarm.title)
        self.scheduler.update(alarm, cron=(hour, minute))

    def save(self):
        ql_fs.touch(
            self.ALARM_DB_FILE_PATH,
            {
                'alarms': [
                    {
                        'title': alarm.title,
                        'hour': alarm.hour,
                        'minute': alarm.minute,
                        'weekdays': alarm.weekdays,
                        'ring': alarm.ring,
                        'shake': alarm.shake,
                        'valid': alarm.valid
                    }
                    for alarm in self.alarms
                ]
            }
        )
