from typing import List, Tuple
from datetime import datetime
from ortools.sat.python import cp_model
from src.models.task import Task
from src.utils.excel_handler import ExcelHandler
from src.utils.date_converter import DateConverter

class TaskScheduler:
    def __init__(self, num_workers: int, workday_hours: int, start_date: datetime):
        self.tasks: List[Task] = []
        self.num_workers = num_workers
        self.workday_hours = workday_hours
        self.start_date = start_date
        self.excel_handler = ExcelHandler()
        self.date_converter = DateConverter(start_date)

    def load_tasks_from_excel(self, file_path: str, sheet_name: str):
        self.tasks = self.excel_handler.load_tasks(file_path, sheet_name)

    def _parse_predecessors(self, predecessor_str: str) -> List[int]:
        if not predecessor_str or str(predecessor_str).lower() == 'nan':
            return []
        return [int(p) for p in str(predecessor_str).split(',') if p.strip().isdigit()]

    def solve_scheduling(self) -> List[Tuple[int, int, int]]:
        model = cp_model.CpModel()
        start_times = []
        end_times = []
        intervals = []

        for task in self.tasks:
            start = model.NewIntVar(0, 100000, f'start_{task.id}')
            end = model.NewIntVar(0, 100000, f'end_{task.id}')
            interval = model.NewIntervalVar(start, task.duration, end, f'interval_{task.id}')
            start_times.append(start)
            end_times.append(end)
            intervals.append(interval)

        # 依存関係の追加
        for task in self.tasks:
            for predecessor_id in task.predecessors:
                predecessor_index = next((i for i, t in enumerate(self.tasks) if t.id == predecessor_id), None)
                if predecessor_index is not None:
                    model.Add(end_times[predecessor_index] <= start_times[self.tasks.index(task)])

        # リソース制約
        model.AddCumulative(intervals, [1] * len(intervals), self.num_workers)

        # 最速完了時間の最小化
        makespan = model.NewIntVar(0, 100000, 'makespan')
        model.AddMaxEquality(makespan, end_times)
        model.Minimize(makespan)

        # 解の取得
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        results = []
        if status == cp_model.OPTIMAL:
            for i, task in enumerate(self.tasks):
                start_time = solver.Value(start_times[i])
                end_time = solver.Value(end_times[i])
                
                # CP-SATによる推定開始・終了時間の設定
                task.cp_estimated_start_time, task.cp_estimated_end_time = self.date_converter.convert_to_datetime(start_time, end_time)
                
                # 手動入力の予想終了時間との差を計算
                if task.target_end_time:
                    task.difference = (task.target_end_time - task.cp_estimated_end_time).total_seconds() / 3600
                results.append((task.id, start_time, end_time))
        
        return results

    def export_results_to_excel(self, file_path: str, sheet_name: str, scheduling_results: List[Tuple[int, int, int]]):
        self.excel_handler.export_results(file_path, sheet_name, self.tasks, scheduling_results)