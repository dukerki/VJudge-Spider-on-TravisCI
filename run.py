# Most of this code is based on Kate123Wong-2873311074@qq.com
from selenium import webdriver
import requests
import time
from lxml import etree
import sys
from selenium.common.exceptions import InvalidArgumentException
import pdb;

this_url = ""
pre_url = ""
REPO="VJudge-Spider-on-TravisCI"
out="out.csv"

def readin():
    global this_url
    global pre_url
    f = open("url.txt", "r")
    this_url = f.readline()
    pre_url = f.readline()
    f.close()


class contestant:
    def __lt__(self, other):
        return float(self.score_sum) > float(other.score_sum)

    name = ""  # 姓名
    accepted = 0  # 解题个数（不包括only AC和fb）
    accepted_fb = 0  # 最快题解个数
    upsolved = 0  # 补题个数
    only_ac = 0  # 唯一AC题个数
    rank = 0  # 排名

    score_ac = 0  # 过题分
    score_extra = 0  # 附加分
    score_up = 0  # 补题分
    score_rank = 0  # 排名奖励分
    score_this = 0
    score_sum = 0  # 总分

    # 总分 = 过题分 + 附加分 + 补题分+ 排名奖励分

    # 过题分:
    # 1分

    # 附加分
    # Only AC: +0.5    max(1)
    # FB:      +0.2    max(1)

    # 补题分
    # up:      +0.5

    # 排名奖励分
    # < 10%: +4
    # < 30%: +3
    # < 60%: +2
    # else : +1

    # 本场得分：
    # 过题分
    # only AC
    # FB
    # 排名奖励


def getResultOfUrl(url, ifShowUpsloved):

    # options = webdriver.ChromeOptions()
    # options.binary_location = '/usr/bin/chromium-browser'
    # #All the arguments added for chromium to work on selenium
    # options.add_argument("--no-sandbox") #This make Chromium reachable
    # options.add_argument("--no-default-browser-check") #Overrides default choices
    # options.add_argument("--no-first-run")
    # options.add_argument("--disable-default-apps")
    # browser = webdriver.Chrome('/home/travis/virtualenv/python3.7.1/chromedriver',options=options)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    try:
        browser.get(url)
    except InvalidArgumentException:
        print("No input or Error While Requesting")
        return []
    time.sleep(3)

    browser.find_element_by_xpath('//*[@id="btn-setting"]').click()
    if ifShowUpsloved:
        browser.execute_script(
            "document.getElementsByTagName('label')[2].click()")
    selector = etree.HTML(browser.page_source)

    student = []  # 统计所有学生的信息
    work_student = {}  # 题 ==> 学生，用于统计only ac
    row = selector.xpath(
        "//*[@id='contest-rank-table']/tbody")[0].getchildren()

    for i in range(len(row)):
        stu = contestant()
        column = row[i].getchildren()

        for j in range(len(column)):
            classes = (column[j].xpath("./@class")[0])

            classes = str(classes).split(" ")
            # 统计ac题目的人数
            if "accepted" in classes:
                if str(work_student.get(chr(ord('A') + j - 4))) == "None":
                    work_student.setdefault(chr(ord('A') + j - 4), [])

                work_student[chr(ord('A') + j - 4)].append(stu.name)

            if "team" in classes:
                if len(column[j].xpath("./div/a/span/text()"))<1 :
                    print("invaild name contestant") # 如果没有nickname，就不会统计
                    continue

                stu.name = (str(column[j].xpath(
                    "./div/a/span/text()")[0])).replace('(', '').replace(')', '').replace(' ', '')
                    
            if "accepted" in classes:
                stu.accepted += 1

            if "fb" in classes:
                stu.accepted_fb += 1

            if "upsolved" in classes:
                stu.upsolved += 1

        student.append(stu)

    # 统计only ac
    for i in work_student.keys():
        if len(work_student[i]) == 1:
            for stu in student:
                if stu.name == work_student[i][0]:
                    stu.only_ac = stu.only_ac + 1
                    break

    # 计算一些score，rank涉及到上次的补题分，故暂时不算
    for stu in student:
        stu.score_ac = stu.accepted
        stu.score_up = stu.upsolved * 0.5
        stu.score_extra = (stu.accepted_fb - stu.only_ac) * \
                          0.2 + stu.only_ac * 0.5
        stu.score_sum = stu.score_ac + stu.score_extra
        stu.score_this = stu.score_sum
    
    # 计算本场来了的比赛排名奖励分：
    students = sorted(student)
    if not ifShowUpsloved:
        for stu in students:
            rate = (students.index(stu) + 1) / students.__len__()
            if rate < 0.1:
                stu.score_rank = 4
            elif rate < 0.3:
                stu.score_rank = 3
            elif rate < 0.6:
                stu.score_rank = 2
            else:
                stu.score_rank = 1
    return students


def getResultHaveUPsolved(students_this, students_pre):
    # 加上次的补题分
    students = []

    for stu in students_this:
        tmpstu = stu
        for stu_pre in students_pre:
            if stu_pre.name == stu.name:
                tmpstu.upsolved = stu_pre.upsolved
                tmpstu.score_up = stu_pre.score_up
                tmpstu.score_sum += tmpstu.score_up
                students_pre.remove(stu_pre)

        students.append(tmpstu)
    
    # 维护本次没有来，但是上次来了的同学的信息
    for stu_pre in students_pre:
        tmpstu = contestant()
        tmpstu.upsolved = stu_pre.upsolved
        tmpstu.score_up = stu_pre.score_up
        tmpstu.score_sum += tmpstu.score_up
        tmpstu.name=stu_pre.name
        students.append(tmpstu)

    return students


def getResult(students):
    # 加上之前的sum值,排序，得到排名奖励分和rank
    with open(out, "r", encoding="utf-8") as f:
        f.readline()  # 吞掉标题行
        for line in f:
            studentFromScv = str(line).replace('\n', '').split(',')

            findit = False
            for stu in students:
                if stu.name == studentFromScv[0]:
                    stu.score_sum = float(stu.score_sum) + \
                                    float(studentFromScv[7])
                    findit = True
                    break
            if findit is False:
                tmpstu = contestant()
                tmpstu.name = studentFromScv[0]
                if(len(studentFromScv)<8):
                    print("out.csv文件中可能有不满足列格式的行")
                    exit(1)
                tmpstu.score_sum = studentFromScv[7]
                students.append(tmpstu)
    f.close()

    for stu in students:
        stu.score_sum = float(stu.score_sum) + stu.score_rank
        stu.score_this = float(stu.score_this) + float(stu.score_rank)

    students = sorted(students)
  
    for stu in students:
        stu.rank = students.index(stu) + 1
    return students


if __name__ == '__main__':
    readin()
    students_this = getResultOfUrl(this_url, False)  # 本次页面统计，不统计upsloved的成绩
    print("this_url success")
    students_pre = getResultOfUrl(pre_url, True)  # 对上次比赛页面进行统计，主要得到upsloved成绩
    print("pre_url success")
    # 整合本次AC，only AC， fb成绩和上次比赛的补题成绩
    students = getResultHaveUPsolved(students_this, students_pre)
    students = getResult(students)
    
    f = open(out, 'w', encoding="utf8")
    print('Name, Accepted, OnlyAC, FirstBlood, ThisRankScore, Upsolved, Score, SumScore, Rank', file=f)
    
    for stu in students:
        if stu.name != '':
            print('{0},{1},{2},{3},{4},{5},{6:.1f},{7:.1f},{8}'.format(stu.name, stu.accepted, stu.only_ac,
                                                                       stu.accepted_fb, stu.score_rank, stu.upsolved,
                                                                       stu.score_this, stu.score_sum, stu.rank),
                  file=f)
    f.close()
    print("Finished")
