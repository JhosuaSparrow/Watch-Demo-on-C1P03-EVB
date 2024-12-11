import lvgl as lv


class Font(object):
    flash_port = 0
    db = {}

    @classmethod
    def get_font_by_name(cls, name):
        # name: <字体名称> + <子模高度>
        height = int(name.split('_')[-1])
        lv_font = lv.style_t()
        lv_font.init()
        lv_font.set_text_font_v2("{}.bin".format(name), height, cls.flash_port)
        return lv_font

    @classmethod
    def get(cls, font_name):
        if font_name not in cls.db:
            cls.db[font_name] = cls.get_font_by_name(font_name)
        return cls.db[font_name]
