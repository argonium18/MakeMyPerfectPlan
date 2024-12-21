from datetime import datetime, timedelta
from typing import Tuple

class DateConverter:
    def __init__(self, start_date: datetime):
        self.start_date = start_date
        self.WORK_START_HOUR = 9
        self.LUNCH_PERIOD_START = 3
        self.LUNCH_PERIOD_END = 4
        self.WORK_HOURS_PER_DAY = 9

    def convert_to_datetime(self, task_start: int, task_end: int) -> Tuple[datetime, datetime]:
        """タスクの開始時間と終了時間をdatetime型に変換"""
        def adjust_for_lunch(hours: int) -> int:
            """昼休憩を考慮して実際の経過時間を計算"""
            days = hours // self.WORK_HOURS_PER_DAY
            remaining_hours = hours % self.WORK_HOURS_PER_DAY
            if remaining_hours > self.LUNCH_PERIOD_START:
                hours += 1
            return hours + days

        start_hours = adjust_for_lunch(task_start)
        end_hours = adjust_for_lunch(task_end)

        start_days = start_hours // self.WORK_HOURS_PER_DAY
        start_remaining = start_hours % self.WORK_HOURS_PER_DAY
        end_days = end_hours // self.WORK_HOURS_PER_DAY
        end_remaining = end_hours % self.WORK_HOURS_PER_DAY

        if end_remaining == 0 and end_hours != 0:
            end_days -= 1
            end_remaining = self.WORK_HOURS_PER_DAY
        
        start_time = (self.start_date + timedelta(days=start_days))
        start_time = start_time.replace(hour=self.WORK_START_HOUR)
        start_time += timedelta(hours=start_remaining)

        end_time = (self.start_date + timedelta(days=end_days))
        end_time = end_time.replace(hour=self.WORK_START_HOUR)
        end_time += timedelta(hours=end_remaining)

        return start_time, end_time