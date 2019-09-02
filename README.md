# Catch_CQU_CoursTable
从重庆大学教务网爬取课表信息，并转存为ics文件,方便导入到手机系统自带的日历APP。

# Usage
## 搭配环境
如果未安装anaconda3，你可能需要在Python 3.7上安装`bs4`，`icalendar`库。<br>

## 运行
需要修改主函数中的相关参数（学号、密码等），然后直接`python main.py`，即可得到ics文件。<br>
在iPad、华为 honor v9上打开ics文件可直接导入到系统日历APP，然而OnePlus 7的系统日历不支持导入ics文件，需要借助[iCal import/Export](https://play.google.com/store/apps/details?id=tk.drlue.icalimportexport&hl=zh) App导入到系统日历中。


# Reference
1.<https://github.com/fengkx/iCal-2018/blob/master/ical.py><br>
2.<https://cloverii.github.io/2017-05-04/a-python-crawler-for-getting-school-timetable/><br>
3.<https://www.programcreek.com/python/example/56510/icalendar.Event><br>
4.<https://www.programcreek.com/python/example/68670/icalendar.Calendar><br>
