[app]

title = DailyExpense Manager

package.name = dailyexpense

package.domain = org.shribel


source.dir = .


requirements = python3,kivy,openpyxl,reportlab,matplotlib


orientation = portrait


android.api = 35

android.minapi = 23


android.archs = arm64-v8a


android.permissions =
    INTERNET,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE
