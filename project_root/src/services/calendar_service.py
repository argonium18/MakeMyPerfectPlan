import pandas as pd
import jpholiday
import numpy as np

class CalendarService:
    @staticmethod
    def get_calendar_data(year, project_start_date, project_end_date):
        """
        指定された年と期間に基づいてカレンダーデータを取得します。
        
        Args:
            year (int): 年度
            project_start_date (datetime): プロジェクトの開始日
            project_end_date (datetime): プロジェクトの終了日

        Returns:
            pd.DataFrame: カレンダーデータ
        """
        return get_japanese_calendar(year, project_start_date, project_end_date)

def get_japanese_calendar(year, project_start_date, project_end_date):
    """
    日本のカレンダー情報を生成する関数。
    
    Args:
        year (int): 年度
        project_start_date (datetime): プロジェクトの開始日
        project_end_date (datetime): プロジェクトの終了日
    
    Returns:
        pd.DataFrame: カレンダーデータフレーム
    """
    # 全日付を生成
    dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31")
    df = pd.DataFrame({'date': dates})
    
    # 曜日情報を追加
    df['weekday'] = df['date'].dt.weekday  # 0:月曜日, ..., 6:日曜日
    df['weekday_name'] = df['date'].dt.day_name(locale='ja_JP')  # 日本語で曜日名

    # 曜日名から「曜日」を削除
    df['weekday_name'] = df['weekday_name'].str.replace("曜日", "")
    
    # 祝日情報を追加
    df['holiday_name'] = df['date'].apply(lambda x: jpholiday.is_holiday_name(x))
    
    # 土曜日・日曜日の名前を祝日情報に追加
    df['holiday_name'] = df['holiday_name'].where(~df['weekday_name'].isin(["土", "日"]), df['weekday_name'])

    # 祝日フラグを追加
    df['holiday'] = np.where(df['holiday_name'].notna(), '祝', '')

    # 日付ごとの情報を整理
    df["day"] = df["date"].dt.day
    columns = ["date", "day", "weekday_name", "holiday_name", "holiday"]
    df = df[columns]

    # 指定された期間でフィルタリング
    df = df.loc[
        (df['date'] >= project_start_date) & (df['date'] <= project_end_date)
    ].copy()

    return df


project_start_date = '2025-01-11'
project_end_date = '2025-01-31'
calendar_df = CalendarService.get_calendar_data(2025, project_start_date, project_end_date)

