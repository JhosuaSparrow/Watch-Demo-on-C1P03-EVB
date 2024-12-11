import lvgl as lv


lv_font_32_simsum_style = lv.style_t()
lv_font_32_simsum_style.init()
lv_font_32_simsum_style.set_text_font_v2("lv_font_32_simsum.bin", 32, 0)


obj = lv.obj()


label0 = lv.label(obj)
label0.set_text('9876543210')


label = lv.label(obj)
label.add_style(lv_font_32_simsum_style, lv.PART.MAIN | lv.STATE.DEFAULT)
label.set_text('0123456789')
label.center()


lv.scr_load(obj)
