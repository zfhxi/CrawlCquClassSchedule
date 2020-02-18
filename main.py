#!/home/julian/Apps/anaconda3/envs/mylab/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   main_dev.py
@Time    :   2019/09/09 23:56:51
@Author  :   zfhxi
@Version :   v1.2.1
@Contact :   zifeihanxi@hotmailcom
'''



import http.cookiejar as cookielib
import urllib.request as urllibre
import urllib.parse as urllibpar
import hashlib
from bs4 import BeautifulSoup
import re
from icalendar import Calendar, Event, vDatetime
from datetime import date, datetime, timedelta
import pytz


def pwd_md5(sid, pwd):
    '''
    提供密码加密后的序列
    '''
    schoolcode = '10611'

    def get_md5(str):
        '''
        提供MD5值
        '''
        return hashlib.md5(str.encode("utf-8")).hexdigest()
    return get_md5(sid + get_md5(pwd)[0:30].upper()+schoolcode)[0:30].upper()


def stu_login(index_url, stu_id, stu_pwd):
    '''
    通过学号密码登录教务网
    '''
    cookie = cookielib.CookieJar()
    opener = urllibre.build_opener(urllibre.HTTPCookieProcessor(cookie))
    postdata = urllibpar.urlencode({
        'Sel_Type': 'STU',
        'txt_dsdsdsdjkjkjc': stu_id,
        'efdfdfuuyyuuckjg': pwd_md5(stu_id, stu_pwd)
    }).encode("utf-8")
    req = urllibre.Request(url=index_url, data=postdata)
    opener.open(req)
    return opener


def cat_crs_tab_webpage(login_opener, semester, crs_tab_url):
    '''
    查询某学期课表
    '''
    postdata = urllibpar.urlencode({
        'Sel_XNXQ': semester,
        'rad': 'on',
        'px': '1'
    }).encode("utf-8")
    req = urllibre.Request(url=crs_tab_url, data=postdata)
    res = login_opener.open(req)
    page_str = res.read().decode('gb2312')
    return page_str


def get_first_week_timeline(first_day):
    '''
    根据开学第一天获取第一周的作息表
    '''
    time_line = []
    first_day_timeline = [
        datetime(first_day.year, first_day.month, first_day.day, 8, 30),
        datetime(first_day.year, first_day.month, first_day.day, 9, 25),
        datetime(first_day.year, first_day.month, first_day.day, 10, 30),
        datetime(first_day.year, first_day.month, first_day.day, 11, 25),
        datetime(first_day.year, first_day.month, first_day.day, 14, 00),
        datetime(first_day.year, first_day.month, first_day.day, 14, 55),
        datetime(first_day.year, first_day.month, first_day.day, 16, 00),
        datetime(first_day.year, first_day.month, first_day.day, 16, 55),
        datetime(first_day.year, first_day.month, first_day.day, 19, 00),
        datetime(first_day.year, first_day.month, first_day.day, 19, 55),
        datetime(first_day.year, first_day.month, first_day.day, 20, 50)
    ]
    time_line.append(first_day_timeline)
    i = 0
    while(i < 6):
        i += 1
        tmp_day_timeline = []
        for dt in time_line[-1]:
            tmp_day_timeline.append(dt+timedelta(days=1))
        time_line.append(tmp_day_timeline)
    return time_line


def cat_course_table_as_lists(doc, infoDictList):
    '''
    从html文档中提取课程表信息,并转为列表

    返回一个嵌套列表，第一层列表的元素包含每门课程的信息，
    第二层列表的元素是课程名，授课老师，上课周次，上课时间，上课地点
    如: [['[IDUE149]能源互联网和深度学习应用', '余娟', '19-21', '一[1-4节]', 'D1135'],
     ['[SE21101]软件工程导论', '刘礼', '1-7', '一[1-2节]', 'D1414'], ...]
    '''
    soup = BeautifulSoup(doc, 'html.parser')
    tables = soup.find_all('tbody')
    # 非实验课程
    tab = tables[0]
    crs_table = []
    # 爬取每一行
    trs = tab.find_all('tr')
    for tr in trs:
        row = []
        td = tr.find_all('td')
        del td[0]
        del td[1:8]
        for p_td in td[:]:
            # 获取标签的文本内容
            cell = p_td.getText().split('\n')[0]
            # 如果文本不为空，加入table列表
            if len(cell) > 0:
                row.append(cell)
            # 如果获取标签的文本为空，那么推测标签有hidevalue属性,并且hidevalue的值同上一标签
            else:
                cell = p_td.get('hidevalue')
                row.append(cell)
        crs_table.append(row)
    # 实验课
    if(len(tables) == 2):
        tab = tables[1]
        trs = tab.find_all('tr')
        for tr in trs:
            row = []
            td = tr.find_all('td')
            del td[0]
            del td[1:6]
            del td[2]
            for p_td in td[:]:
                cell = p_td.getText().split('\n')[0]
                if len(cell) > 0:
                    row.append(cell)
                else:
                    cell = p_td.get('hidevalue')
                    row.append(cell)
            crs_table.append(row)
    return crs_table


def cat_course_table_as_dicts(crs_tab):
    '''
    将课程信息以字典形式存储

    如: [{'课程名称': '[IDUE149]能源互联网和深度学习应用', '授课老师': '余娟', '星期': '一',
    '节数': [1, 2, 3, 4], '课程周次': [19, 20, 21], '上课地点': 'D1135'},
     {'课程名称': '[SE21101]软件工程导论', '授课老师': '刘礼', '星期': '一',
     '节数': [1, 2], '课程周次': [1, 2, 3, 4, 5, 6, 7], '上课地点': 'D1414'},...]
    '''
    crs_lists = []
    for one_crs in crs_tab:
        t_dict = {}
        t_dict.update({'课程名称': one_crs[0].split(']')[1]})
        t_dict.update({'授课老师': one_crs[1]})
        t_dict.update({'星期': one_crs[3][0]})

        # 从字符串中分割出课程开始的节数、结束的节数
        count = re.split(r'-', one_crs[3][2:-2])
        n_seg = list(map(lambda x: int(x), count))
        seg_list = list(range((n_seg[0]), n_seg[len(n_seg)-1]+1))
        t_dict.update({'节数': seg_list})

        def get_weeks(str):
            '''
            得到课程周次

            如字符串形式的'4-6,9-11'，会被转为列表[4,5,6,9,10,11]
            '''
            cut_by_dot = re.split(r',', str)
            segs = []
            for ele in cut_by_dot:
                n_seg = re.split(r'-', ele)
                # 整型化
                n_seg = list(map(lambda x: int(x), n_seg))
                seg_list = list(range((n_seg[0]), n_seg[len(n_seg)-1]+1))
                segs.extend(seg_list)
            # 去重复
            segs = list(set(segs))
            return segs

        t_dict.update({'课程周次': get_weeks(one_crs[2])})
        t_dict.update({'上课地点': one_crs[4]})
        crs_lists.append(t_dict)
    return crs_lists


def ics_maker(crs_dicts, Time):
    '''
    将课程字典列表转换为ics

    刑如:
    BEGIN:VEVENT
    SUMMARY:[IDUE149]能源互联网和深度学习应用
    DTSTART;TZID=Asia/Shanghai;VALUE=DATE-TIME:20200106T083000
    DTEND;TZID=Asia/Shanghai;VALUE=DATE-TIME:20200106T091500
    DESCRIPTION:余娟
    LOCATION:D1135
    END:VEVENT
    '''
    # 映射
    Week = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7}
    # 时区指定
    tz_utc_8 = pytz.timezone('Asia/Shanghai')
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('x-wr-timezone', tz_utc_8)
    for one_crs in crs_dicts:
        for lesson_num in one_crs['节数']:
            if(lesson_num > 11):
                lesson_num = 11
            for week_num in one_crs['课程周次']:
                tmp_event = Event()
                tmp_event.add('summary', one_crs['课程名称'])
                # 取消日程详情项显示授课老师姓名, 原因: 部分日历程序不显示详情
                tmp_event.add(
                    'location', '%s %s 第%d周' % (one_crs['上课地点'],one_crs['授课老师'],week_num))
                # tmp_event.add('description', one_crs['授课老师'])

                # 根据周次计算课程开始时间
                day_num = Week[one_crs['星期']]
                crs_time_begin = Time[day_num-1][lesson_num-1] + \
                    timedelta(days=7*(week_num-1))
                crs_time_end = crs_time_begin+timedelta(minutes=45)
                tmp_event.add('dtstart', vDatetime(crs_time_begin))
                tmp_event.add('dtend', vDatetime(crs_time_end))

                cal.add_component(tmp_event)
    return cal


#############################


if __name__ == "__main__":
    # 学号
    sid = '2017xxxx'
    # 密码
    pwd = '**********'
    # 当前学期代号
    current_semester = '20191'
    # 开学第一天
    first_day = date(2020, 2, 17)
    # 教务网登录主页
    index_url = 'http://202.202.1.41/_data/index_login.aspx'
    # 课表查看页面
    crstable_url = 'http://202.202.1.41/znpk/Pri_StuSel_rpt.aspx'

    ##-----------------------------------------------------------##

    # 第一周的时间线
    first_week = get_first_week_timeline(first_day)
    # 登录
    login_opener = stu_login(index_url, sid, pwd)
    # 捕获课表页面
    crs_tab_page_str = cat_crs_tab_webpage(
        login_opener, current_semester, crstable_url)
    # 从课表页面获取课程信息列表
    crs_tab = cat_course_table_as_lists(crs_tab_page_str, 0)
    # 将信息列表转换字典
    crs_dicts = cat_course_table_as_dicts(crs_tab)
    # 将课程字典转换为ics保存
    my_cal = ics_maker(crs_dicts, first_week)
    f = open('crs_v1.0.ics', 'wb')
    f.write(my_cal.to_ical())
    f.close()
    print('Script has been executed!')
