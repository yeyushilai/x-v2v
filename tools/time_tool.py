#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import random
from typing import Any


class TimeTool:

    @classmethod
    def gen_random_today_date(cls) -> str:
        """ 生成随机的今日时间 """
        random_hour = str(random.randint(0, 23))
        random_min = str(random.randint(0, 59))
        random_second = str(random.randint(0, 59))

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        today_time = '%s %s:%s:%s' % (today, random_hour, random_min, random_second)
        return today_time

    @classmethod
    def is_valid_date(cls, date_str: str) -> bool:
        """ 验证日期格式 """
        try:
            if ":" in date_str:
                time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False
        return True

    @classmethod
    def timestamp_to_date(cls, ts: int) -> str:
        """ 将时间戳转换为日期 """
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def timestamp_to_date_without_second(cls, ts: int) -> str:
        """ 将时间戳转换为日期 """
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

    @classmethod
    def timestamp_to_day(cls, ts: int) -> str:
        """ 将时间戳转换为天 """
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    @classmethod
    def date_to_timestamp(cls, date_str: str) -> int:
        """ 将日期转换为时间戳, date_str的格式为 '%Y-%m-%d %H:%M:%S' """
        return int(time.mktime(time.strptime(date_str, '%Y-%m-%d %H:%M:%S')))

    @classmethod
    def day_to_timestamp(cls, day_str: str) -> int:
        """ 将天转换为时间戳, date_str的格式为 '%Y-%m-%d' """
        return int(time.mktime(time.strptime(day_str, '%Y-%m-%d')))

    @classmethod
    def datetime_to_str(cls, dt: datetime.datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """ 将datetime类型转换为字符串类型 """
        return dt.strftime(format_str)

    @classmethod
    def datetime_to_datetime(cls, dt: datetime.datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> datetime.datetime:
        """ 将datetime类型转换为字符串类型，然后再转换为datetime类型，主要是为了把秒去掉 """
        dt_str = dt.strftime(format_str)
        return datetime.datetime.strptime(dt_str, format_str)

    @classmethod
    def get_today_weekday(cls) -> int:
        """ 获取今天是星期几 """
        return datetime.datetime.now().weekday()

    @classmethod
    def get_weekday_by_date(cls, date: datetime.date) -> int:
        """ 获取指定日期是星期几 """
        return date.weekday()

    @classmethod
    def get_now_day(cls) -> str:
        """ 获得今天的日期 """
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def get_now_hour(cls) -> str:
        """ 获得现在的小时 """
        return datetime.datetime.now().strftime("%Y-%m-%d %H")

    @classmethod
    def get_now_datetime(cls) -> datetime.datetime:
        """ 获取当前时间 """
        return datetime.datetime.now()

    @classmethod
    def get_now_minute(cls) -> str:
        """ 获得现在的分钟 """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    @classmethod
    def get_now_second(cls) -> str:
        """ 获得现在的秒 """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_now_timestamp(cls) -> int:
        """ 获取当前时间戳 """
        return int(time.time())

    @classmethod
    def get_now_datetime_str(cls) -> str:
        """ 获得现在的时间字符串 """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_before_day(cls, number: int = 1, format_str: str = "%Y-%m-%d") -> str:
        """ 获取前几天的日期 """
        today = datetime.date.today()
        oneday = datetime.timedelta(days=number)
        yesterday = today - oneday
        return yesterday.strftime(format_str)

    @classmethod
    def get_before_day_by_date(cls, date: Any, number: int = 1, format_str: str = "%Y-%m-%d") -> str:
        """ 获取指定日期前几天的日期 """
        oneday = datetime.timedelta(days=number)
        yesterday = date - oneday
        return yesterday.strftime(format_str)

    @classmethod
    def get_after_day(cls, number: int = 1, format_str: str = "%Y-%m-%d") -> str:
        """ 获取后几天的日期 """
        today = datetime.date.today()
        oneday = datetime.timedelta(days=number)
        tomorrow = today + oneday
        return tomorrow.strftime(format_str)

    @classmethod
    def get_after_day_by_date(cls, date: Any, number: int = 1, format_str: str = "%Y-%m-%d") -> str:
        """ 获取指定日期后几天的日期 """
        oneday = datetime.timedelta(days=number)
        tomorrow = date + oneday
        return tomorrow.strftime(format_str)

    @classmethod
    def is_weekday(cls, date: Any = None) -> bool:
        """ 判断是工作日还是周末 """
        if not date:
            date = datetime.datetime.now()
        return True if date.weekday() <= 4 else False

    @classmethod
    def is_today(cls, ts: int) -> bool:
        """ 时间戳对应的日期是不是今天 """
        now = datetime.datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        today_start_ts = int(time.mktime(time.strptime(today_str, "%Y-%m-%d")))
        today_end_ts = today_start_ts + 86400
        if today_start_ts <= ts < today_end_ts:
            return True
        else:
            return False

    @classmethod
    def is_lastday(cls, ts: int) -> bool:
        """ 时间戳对应的日期是不是昨天 """
        now = datetime.datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        today_start_ts = int(time.mktime(time.strptime(today_str, "%Y-%m-%d")))
        last_day_start_ts = today_start_ts - 86400
        if last_day_start_ts <= ts < today_start_ts:
            return True
        else:
            return False

    @classmethod
    def is_between_start_and_end_ts(cls, ts: int, start_ts: int, end_ts: int) -> bool:
        """ 时间戳是否在开始和结束时间戳之间 """
        if start_ts <= ts <= end_ts:
            return True
        else:
            return False

    @classmethod
    def get_week_start_day(cls, current_datetime: datetime.date = None) -> datetime.date:
        """ 获取本周周一的日期 """
        if not current_datetime:
            current_datetime = datetime.datetime.now().date()
        current_week_num = current_datetime.weekday()
        start_datetime = current_datetime - datetime.timedelta(days=current_week_num)
        return start_datetime

    @classmethod
    def get_week_end_day(cls, current_datetime: datetime.date = None) -> datetime.date:
        """ 获取本周周日的日期 """
        if not current_datetime:
            current_datetime = datetime.datetime.now().date()
        current_week_num = current_datetime.weekday()
        end_datetime = current_datetime + datetime.timedelta(days=6 - current_week_num)
        return end_datetime

    @classmethod
    def get_last_week_start_day(cls) -> datetime.date:
        """ 获取上周周一的日期 """
        week_start_date = cls.get_week_start_day()
        last_week_start_date = week_start_date - datetime.timedelta(days=7)
        return last_week_start_date

    @classmethod
    def get_last_week_end_day(cls) -> datetime.date:
        """ 获取上周周日的日期 """
        week_start_date = cls.get_week_start_day()
        last_week_end_date = week_start_date - datetime.timedelta(days=1)
        return last_week_end_date

    @classmethod
    def get_last_month_start_day(cls) -> datetime.date:
        """ 获取上个月第一天的日期 """
        today = datetime.date.today()
        last_month_end_day = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
        last_month_start_day = datetime.date(last_month_end_day.year, last_month_end_day.month, 1)
        return last_month_start_day

    @classmethod
    def get_last_month_end_day(cls) -> datetime.date:
        """ 获取上个月最后一天的日期 """
        today = datetime.date.today()
        last_month_end_day = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
        return last_month_end_day

    @classmethod
    def get_current_month_start_day(cls) -> datetime.date:
        """ 获取当前月第一天的日期 """
        today = datetime.date.today()
        return datetime.date(today.year, today.month, 1)

    @classmethod
    def get_last_quarter_start_day(cls) -> datetime.date:
        """ 获取上个季度第一天的日期 """
        today = datetime.date.today()
        month = today.month

        if month in [1, 2, 3]:
            # 1月、2月、3月
            year = today.year - 1
            last_quarter_start_day = datetime.date(year, 10, 1)
            last_quarter_end_day = datetime.date(year, 12, 31)
        elif month in [4, 5, 6]:
            # 4月、5月、6月
            year = today.year
            last_quarter_start_day = datetime.date(year, 1, 1)
            last_quarter_end_day = datetime.date(year, 3, 31)
        elif month in [7, 8, 9]:
            # 7月、8月、9月
            year = today.year
            last_quarter_start_day = datetime.date(year, 4, 1)
            last_quarter_end_day = datetime.date(year, 6, 30)
        elif month in [10, 11, 12]:
            # 10月、11月、12月
            year = today.year
            last_quarter_start_day = datetime.date(year, 7, 1)
            last_quarter_end_day = datetime.date(year, 9, 30)
        else:
            raise Exception('month error')

        return last_quarter_start_day

    @classmethod
    def get_last_quarter_end_day(cls) -> datetime.date:
        """ 获取上个季度最后一天的日期 """
        today = datetime.date.today()
        month = today.month

        if month in [1, 2, 3]:
            # 1月、2月、3月
            year = today.year - 1
            last_quarter_start_day = datetime.date(year, 10, 1)
            last_quarter_end_day = datetime.date(year, 12, 31)
        elif month in [4, 5, 6]:
            # 4月、5月、6月
            year = today.year
            last_quarter_start_day = datetime.date(year, 1, 1)
            last_quarter_end_day = datetime.date(year, 3, 31)
        elif month in [7, 8, 9]:
            # 7月、8月、9月
            year = today.year
            last_quarter_start_day = datetime.date(year, 4, 1)
            last_quarter_end_day = datetime.date(year, 6, 30)
        elif month in [10, 11, 12]:
            # 10月、11月、12月
            year = today.year
            last_quarter_start_day = datetime.date(year, 7, 1)
            last_quarter_end_day = datetime.date(year, 9, 30)
        else:
            raise Exception('month error')

        return last_quarter_end_day

    @classmethod
    def get_datetime_range(cls, start: Any, end: Any, step: int = 86400) -> list[int]:
        """ 获取两个时间戳范围内的所有时间戳列表，步长默认为一天，即86400秒 """
        res = []
        i = start
        while i <= end:
            res.append(i)
            i += step
        return res

    @classmethod
    def get_date_list_by_day_range(cls, start_date: str, end_date: str) -> list[str]:
        """ 根据开始和结束日期获得日期列表 """
        date_list = []
        begin_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    @classmethod
    def get_weekday_list_by_week_range(cls, week_start: Any, week_end: Any) -> list[Any]:
        """ 根据开始和结束的周时间，获得这个时间内的所有的周几列表 """
        weekday_list = []
        date = week_start
        while date <= week_end:
            weekday_list.append(date.weekday())
            date += datetime.timedelta(days=1)
        return weekday_list

    @classmethod
    def get_msec_timestamp(cls) -> int:
        """ 生成秒的时间戳乘以1000 """
        return int(time.time() * 1000)

    @classmethod
    def get_ts_start(cls, ts: int) -> int:
        """ 获取该时间戳当天的起始时间戳 """
        dt = datetime.datetime.fromtimestamp(ts)
        return int(time.mktime(dt.replace(hour=0, minute=0, second=0, microsecond=0).timetuple()))

    @classmethod
    def get_ts_end(cls, ts: int) -> int:
        """ 获取该时间戳当天的结束时间戳 """
        return cls.get_ts_start(ts) + 86400 - 1


if __name__ == '__main__':
    print(TimeTool.get_weekday_list_by_week_range(
        TimeTool.get_last_week_start_day(),
        TimeTool.get_last_week_end_day()
    ))
