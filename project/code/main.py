import uos
from usr.qframe import Application
from usr.ui import gui_service
# from usr.extensions import alarm_service
from usr.scheduler import test_scheduler


def mount_flash():
    ldev = uos.VfsLfs1(32, 32, 32, "ext_fs", 0, 0)
    uos.mount(ldev, '/ext')


def enable_v_spk():
    """听筒vcc"""
    from machine import Pin
    Pin(18, Pin.OUT, Pin.PULL_DISABLE, 1)


def create_app(name='demo', version='1.0.0', config_path='/usr/default.json'):
    _app = Application(name, version=version)
    _app.config.init(config_path)

    gui_service.init_app(_app)
    # alarm_service.init_app(_app)

    return _app


if __name__ == '__main__':
    mount_flash()
    app = create_app()
    app.run()
    enable_v_spk()
    test_scheduler()  # for test
