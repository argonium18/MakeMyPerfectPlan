import openpyxl
import pandas as pd
from typing import List, Tuple
from datetime import datetime
from src.models.task import Task
from src.services.calendar_service import CalendarService
from src.utils.style_constants import ORANGE_FILL, THIN_BORDER

class ExcelHandler:
    def load_tasks(self, file_path: str, sheet_name: str) -> List[Task]:
        """Excelファイルからタスクを読み込む"""
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
        df = df.dropna(how='all')
        
        tasks = []
        for _, row in df.iterrows():
            task = Task(
                id=row['タスク番号'],
                name=row['タスク名'],
                duration=row['工数(予想)'],
                cp_estimated_start_time=row['開始日(予想)'],
                cp_estimated_end_time=row['終了日(予想)'],
                predecessors=self._parse_predecessors(row['先行タスク番号'])
            )
            tasks.append(task)
        return tasks

    def _parse_predecessors(self, predecessor_str: str) -> List[int]:
        if not predecessor_str or str(predecessor_str).lower() == 'nan':
            return []
        return [int(p) for p in str(predecessor_str).split(',') if p.strip().isdigit()]

    def export_results(self, file_path: str, sheet_name: str, tasks: List[Task], scheduling_results: List[Tuple[int, int, int]]):
        """結果をExcelファイルに出力する"""
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        
        project_start_date = '2025-01-11'
        project_end_date = '2025-01-31'
        calendar_df = CalendarService.get_calendar_data(2025, project_start_date, project_end_date)
        
        for row in sheet.iter_rows(min_row=2):
            task_id = row[0].value
            if task_id is None:
                break

            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                row[3].value = task.cp_estimated_start_time
                row[4].value = task.cp_estimated_end_time

                start_col = 10
                for r_idx, date in enumerate(calendar_df["date"], start=start_col):
                    if r_idx < len(row):
                        row[r_idx].border = THIN_BORDER
                        if task.cp_estimated_start_time.date() <= date.date() <= task.cp_estimated_end_time.date():
                            row[r_idx].fill = ORANGE_FILL

        workbook.save(file_path)