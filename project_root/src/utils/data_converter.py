from datetime import datetime, timedelta
from typing import Tuple
from src.services.calendar_service import CalendarService
from src.config.settings import *
import pandas as pd

class DateConverter:
    def __init__(self, start_date: datetime):
        self.start_date = start_date
        self.WORK_START_HOUR = 9
        self.LUNCH_PERIOD_START = 3
        self.LUNCH_PERIOD_END = 4
        self.WORK_HOURS_PER_DAY = 9

    def convert_to_datetime(self, task_start: int, task_end: int) -> tuple[datetime, datetime]:
        """
        タスクの開始時間と終了時間をdatetime型に変換
        """
        WORK_START_HOUR = 9      # 勤務開始時間
        WORK_HOURS_PER_DAY = 9   # 1日の稼働時間時間
        LUNCH_PERIOD_START = 3   # 昼休憩開始時間
        LUNCH_PERIOD_END = 4     # 昼休憩終了時間

        # カレンダー取得
        calendar_df = CalendarService.get_calendar_data(2025, PROJECT_START_DATE, PROJECT_END_DATE)

        # 昼休憩を考慮した時間調整
        def adjust_for_lunch(hours: int) -> int:
            """昼休憩を考慮して実際の経過時間を計算"""
            days = hours // WORK_HOURS_PER_DAY
            remaining_hours = hours % WORK_HOURS_PER_DAY
            if remaining_hours >= LUNCH_PERIOD_START:  # 昼休憩時間を超える場合
                remaining_hours += 1  # 昼休憩時間分を加算
            return days, remaining_hours

        # 休日判定
        def is_holiday(date: datetime) -> bool:
            return calendar_df.loc[calendar_df['date'].dt.date == date.date(), 'holiday_name'].notna().any()

        # 開始時間・終了時間の計算
        start_days, start_remaining = adjust_for_lunch(task_start)
        end_days, end_remaining = adjust_for_lunch(task_end)

        # 終了時間の調整
        if end_remaining == 0 and end_days != 0:
            end_days -= 1
            end_remaining = WORK_HOURS_PER_DAY

        # 開始・終了時刻の設定
        start_date = pd.to_datetime(self.start_date)

        start_time = start_date + timedelta(days=start_days, hours=start_remaining + WORK_START_HOUR)
        end_time = start_date + timedelta(days=end_days, hours=end_remaining + WORK_START_HOUR)

        # 休日を考慮して調整
        while is_holiday(start_time):
            start_time += timedelta(days=1)
        #     start_time = start_time.replace(hour=WORK_START_HOUR)

        while is_holiday(end_time):
            end_time += timedelta(days=1)
        #     end_time = end_time.replace(hour=WORK_START_HOUR)

        return start_time, end_time