from openpyxl.styles import PatternFill, Border, Side

# Excel styles
ORANGE_FILL = PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
)