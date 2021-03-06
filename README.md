# CrawlCquClassSchedule

从重庆大学教务网爬取课表信息，并转存为ics文件,方便导入到手机系统自带的日历APP。

# Preview

以下是结合滴答清单的使用效果：

![](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fd4c808a4-3bd6-406d-a7d6-7919a78be8a6%2FUntitled.png?table=block&id=9cd334f6-2769-4a38-b919-5fef25c8bae4&width=670&cache=v2)

![](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fb5ff44ed-4433-4d93-a7ab-1d42e0a8f17e%2FUntitled.png?table=block&id=825700f6-71fb-417c-bec6-3ac06bfa45f0&width=670&cache=v2)

# Usage

## 搭配环境

如果未安装anaconda3，你可能需要在Python 3.7上安装`bs4`，`icalendar`库。

## 运行

需要修改主函数中的相关参数（学号、密码等），然后直接`python main.py`，即可得到ics文件。

在iPad、华为 honor v9上打开ics文件可直接导入到系统日历APP，然而OnePlus 7的系统日历不支持导入ics文件，需要借助[iCal import/Export](https://play.google.com/store/apps/details?id=tk.drlue.icalimportexport&hl=zh) App导入到系统日历中。

# Reference

1.<https://github.com/fengkx/iCal-2018/blob/master/ical.py>

2.<https://cloverii.github.io/2017-05-04/a-python-crawler-for-getting-school-timetable/>

3.<https://www.programcreek.com/python/example/56510/icalendar.Event>

4.<https://www.programcreek.com/python/example/68670/icalendar.Calendar>
