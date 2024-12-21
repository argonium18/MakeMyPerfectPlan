from src.services.task_scheduler import TaskScheduler
from src.config.settings import (
    DEFAULT_NUM_WORKERS,
    DEFAULT_WORKDAY_HOURS,
    DEFAULT_START_DATE,
    DEFAULT_EXCEL_FILENAME,
    DEFAULT_SHEET_NAME
)

def main():
    scheduler = TaskScheduler(
        num_workers=DEFAULT_NUM_WORKERS,
        workday_hours=DEFAULT_WORKDAY_HOURS,
        start_date=DEFAULT_START_DATE
    )
    
    # Excelからタスクを読み込む
    scheduler.load_tasks_from_excel(DEFAULT_EXCEL_FILENAME, DEFAULT_SHEET_NAME)
    
    # スケジューリングの実行
    scheduling_results = scheduler.solve_scheduling()
    
    # 結果をExcelに出力
    scheduler.export_results_to_excel(DEFAULT_EXCEL_FILENAME, DEFAULT_SHEET_NAME, scheduling_results)

if __name__ == "__main__":
    main()