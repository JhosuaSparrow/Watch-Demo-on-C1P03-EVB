import lvgl as lv
import uos
from usr.ui import gui_service


ldev = uos.VfsLfs1(32, 32, 32, "ext_fs", 0, 0)
uos.mount(ldev, '/ext')


gui_service.load()


obj = lv.obj()


style = lv.style_t()
style.init()
style.set_text_font_v2('lv_font_32.bin', 32, 0)

label1 = lv.label(obj)
label1.set_text('0123456789')
label1.set_size(240, 280)
label1.add_style(style, lv.PART.MAIN | lv.STATE.DEFAULT)
label1.center()


b = lv.btn(obj)
bl = lv.label(b)
bl.set_text('click me!')
b.center()


num = 0


def event_callback(event, obj):
    global num
    num += 1
    obj.set_text('{}'.format(num))


b.add_event_cb(lambda event: event_callback(event, bl), lv.EVENT.CLICKED, None)


lv.scr_load(obj)
