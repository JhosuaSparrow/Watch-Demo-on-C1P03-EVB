"""多国语言"""
import sys_bus


class Language(object):

    __brief__ = 'English'
    __brief_index__ = {
        'Simplified Chinese': 0,  # 简体中文
        'Traditional Chinese': 1,  # 日语
        'Japanese': 2,  # 日语
        'German': 3,  # 德语
        'French': 4,  # 法语
        'Italian': 5,  # 意大利语
        'Spanish': 6,  # 西班牙语
        'Russian': 7,  # 俄语
        'Korean': 8,  # 韩语
        'Portuguese': 9,  # 葡萄牙语
        'Swedish': 10,  # 瑞典语
        'Turkish': 11  # 土耳其语
    }

    database = {
        "Sleep": (
            "睡眠",
            "睡眠",
            "スリープ",
            "Schlaf",
            "Le sommeil",
            "dormire",
            "Dormir",
            "Сон",
            "수면",
            "dormir",
            "sova",
            "uyku",
        ),
        "Total Duration": (
            "总睡眠时间",
            "總持續時間",
            "合計期間",
            "Gesamtdauer",
            "Durée totale",
            "Durata totale",
            "Duración total",
            "Общая продолжительность",
            "총 기간",
            "Duração total",
            "Total varaktighet",
            "Toplam Uzun"
        )
    }

    @classmethod
    def set(cls, brief):
        cls.__brief__ = brief

    @classmethod
    def get(cls):
        return cls.__brief__

    @classmethod
    def get_brief_index(cls):
        return cls.__brief_index__[cls.get()]

    @classmethod
    def translate(cls, text):
        return cls.database[text][cls.get_brief_index()]


def tr(text):
    return Language.translate(text) if Language.get() != 'English' else text
