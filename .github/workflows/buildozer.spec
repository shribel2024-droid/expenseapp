[app]

title = DailyExpense Manager

package.name = dailyexpense

package.domain = org.shribel


source.dir = .


requirements = python3,kivy,openpyxl,reportlab,matplotlib


orientation = portrait


android.permissions =
    INTERNET,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE


android.api = 35

android.minapi = 23


android.archs = arm64-v8a, armeabi-v7a