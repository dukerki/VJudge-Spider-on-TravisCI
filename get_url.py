# 自动从 VJudge 中爬取上次与此次比赛的 rank_url 并自动运行 run.py

import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# 配置区

ContestPrefix = r"CUC-ACM-2025-Winter-Training"
Draw = False  # 是否对每次比赛进行抽奖

# =========================初始化操作===========================

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("window-size=1024,768")
options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument("--no-sandbox")
options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])

# Optional argument, if not specified will search path.
driver = webdriver.Chrome(options=options)

driver.get('https://vjudge.net/contest')

time.sleep(3)  # Let the user actually see something!

# =========================初始化操作===========================

# =========================全局变量区===========================

contests = []  # 整理筛选后按照时间降序排列的比赛
# 搜索出来的全部比赛（包括无关比赛）
global contests_ele
global time_ele
completed_contest_ID = [int]
crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# =========================全局变量区===========================
# 2022-10-12 21:16:17
# 2022-10-12 13:30:00


def get_crt_time() -> str:
    import time

    # 格式化成2016-03-20 11:45:39形式
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def select_elements():
    '''选出后续需要使用的元素'''
    raise driver
    search_box = driver.find_element("xpath",r"/html/body/div[1]/div/div[2]/div/table/thead/tr/th[3]/input")
    
    search_box.send_keys('CUC\n')

    contents_sort = driver.find_element("xpath", r'/html/body/div[1]/div/div[2]/div/table/thead/tr/th[5]')

    contents_sort.click()
    time.sleep(2)
    global contests_ele
    contests_ele = driver.find_elements(By.CLASS_NAME, 'contest_entry')

    set_ele = driver.find_element(
        By.XPATH, '//*[@id="listContest"]/tbody/tr[1]/td[5]/div/span[1]')
    # 第一步：创建一个鼠标操作的对象
    action = ActionChains(driver)
    # 第二步：进行移动
    action.move_to_element(set_ele).perform()
    time.sleep(0.5)
    global time_ele
    time_ele = driver.find_elements(By.CSS_SELECTOR, 'div > span.absolute')


class contest:
    def __init__(self) -> None:
        self.name = ''
        self.begin_time = ''
        self.rank_url = ''
        self.ID = ''
        # self.counted = bool  # 是否已经统计

    def print(self) -> None:
        print(f'{self.name} {self.begin_time} {self.ID} {self.rank_url} {self.counted}')


def select_contests():
    '''从近至远选出本学期的秋季新生比赛，并将其 append 至 contests 列表中'''
    contest_len = int(len(contests_ele))
    # for contest_ele in contests_ele:
    for i in range(contest_len):
        contest_ele = contests_ele[i]
        bg_time = time_ele[i].text
        crt_contest = contest()
        crt_contest.ID = contest_ele.get_attribute('cid')
        crt_contest.name = contest_ele.text

        # 排除非`2022 年新生秋季训练比赛`
        if not re.match(ContestPrefix, crt_contest.name, re.M | re.I):
            continue

        crt_contest.rank_url = 'https://vjudge.net/contest/'+crt_contest.ID+'#rank'
        crt_contest.begin_time = bg_time
        # 判断是否已经统计了
        if crt_contest.ID in completed_contest_ID:
            crt_contest.counted = True
        else:
            crt_contest.counted = False
        crt_contest.print()
        contests.append(crt_contest)  # 加入列表


# def save_in_ContestRecord():
#     '''将记录保存至 ContestRecord.csv'''
#     with open('ContestRecord.csv', 'a+') as f:  # 以在文尾附加的方式打开文件
#         for contest in contests:
#             if contest.counted == False:
#                 f.write(
#                     f"{contest.name}, {contest.begin_time}, {contest.rank_url}, {contest.ID}\n")


def save_in_url_txt_and_run():
    '''读取本次的 url 后，调用师哥的库直接 run'''
    pre_url = str
    # 保存前一次的 url
    with open("url.txt", 'r') as f:
        pre_url = f.readline()
    ContestRecord = open('ContestRecord.csv', 'a+')

# 2022-10-12 21:16:17
# 2022-10-12 13:30:00
    global contests
    contests.reverse()  # 从远及近的处理

    def eight_hours(text: str) -> str:
        from datetime import datetime
        from datetime import timezone
        from datetime import timedelta
        from datetime import timedelta
        temp = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')+timedelta(hours=8)
        return temp.strftime("%Y-%m-%d %H:%M:%S")

    for contest in contests:
        if (int(contest.ID) not in completed_contest_ID) and (contest.begin_time < crt_time):
            # 如果此场比赛还没有被记录 而且 开始时间大于当前时间

            # 先更新 url.txt
            f = open("url.txt", 'w').close()  # 先清空文件
            f = open("url.txt", 'w')
            f.write(f'{contest.rank_url}\n')
            print(f'pre_url: {pre_url}')
            f.write(pre_url)  # 最后一行保存前一次的 url
            f.close()

            # 再跑 run.py
            import run  # 直接调用师哥的库
            print(f'当前处理的是：\n{contest.rank_url}\n{pre_url}\n')
            run.Crawl_and_save()

            # 将结果记录到 ContestRecord.csv 中
            # 由于服务器是用的格林尼治时间，这里需要加上 8 小时
            ContestRecord.write(
                f"{contest.name}, {eight_hours(contest.begin_time)}, {contest.rank_url}, {contest.ID}, {eight_hours(crt_time)}\n")
            if Draw:  # 如果需要抽奖
                import LotteryMachine
                LotteryMachine.rowing_system()  # 抽奖
            pre_url = contest.rank_url+'\n'  # 继续更新 pre_url

    ContestRecord.close()


def check_status():
    '''根据 ContestRecord.csv 检查该比赛是否已经统计
    以此更新 contest.counted 的值'''
    with open('ContestRecord.csv', 'r') as f:
        f.readline()  # 读取标题行
        line = f.readline()
        line = line.strip()  # 去掉结尾空格及换行符
        while line:
            contest_ID = line.replace(' ', '').split(',')[
                3]  # 读取此行的 contest_ID
            completed_contest_ID.append(int(contest_ID))
            line = f.readline()
            line = line.strip()


if __name__ == '__main__':
    check_status()
    select_elements()
    select_contests()
    check_status()
    save_in_url_txt_and_run()

driver.close()  # 关闭浏览器

# name, begin_time, rank_url, ID, update_time
