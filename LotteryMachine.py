import csv
import random

Lucky_Dog_Num = 4  # 中奖人数

ranking_file = 'out.csv'  # 排名
max_participants_num = 40  # 参与抽奖的人数
LuckyDogRecord = 'LuckyDogRecord.csv'  # 记录中奖人的 csv 文档
weights = []  # 中奖概率（权重）
name_list = []


def Peking_Time() -> str:
    '''获取北京时间(github 服务器好像用的是 UTC)'''
    from datetime import datetime, timedelta, timezone
    temp = datetime.now(timezone.utc) + timedelta(hours=8)
    return temp.strftime("%Y-%m-%d %H:%M:%S %a")


def import_name_list():
    '''从 out.csv 导入人员名单'''
    with open(ranking_file, 'r') as f:
        reader = csv.reader(f)
        head_row = next(reader)  # 读取表头
        i = 0
        for row in reader:
            i += 1
            if i > max_participants_num:
                break
            name_list.append(row[0].replace(' ', ''))  # 去除名字间的空格


def cal_probablity():
    '''计算每人的中奖概率'''
    contestant_num = len(name_list)
    print(f'\n=============\n总抽奖人数: {contestant_num}\n=============',)
    with open('Weight.csv', 'w') as f:
        f.write(f'Name, Weight\n')
        for i in range(1, contestant_num+1):
            if i > max_participants_num:
                break
            # 计算某位同学的中奖概率，其中 contestant_num 为总参赛人数，i 为其排名
            # probability = (1-2*i)/(contestant_num *
            #                        contestant_num) + 2/contestant_num
            # # probability = 1/contestant_num
            # probability *= 100
            probability = 100 - i * i / 25  # 抛物线计算概率法
            # print(f'{i}: probability:{probability}')
            # print('_______________________')

            f.write(f'{name_list[i-1]}, ' + format(probability, '.2f') + '\n')
            weights.append(probability)


def Draw_Luckydog() -> list:
    '''根据 weights 和 name_list, 返回中奖人的姓名的列表'''
    Lucky_Dog = random.choices(name_list, weights, k=Lucky_Dog_Num)
    while (len(set(Lucky_Dog)) != Lucky_Dog_Num):  # 避免同一人抽到两次
        Lucky_Dog = random.choices(name_list, weights, k=Lucky_Dog_Num)
    return Lucky_Dog


def query_and_save_in_csv(file_location: str):
    '''查询前一次中奖人员的记录，抽奖，并将结果保存至 LuckyDogRecord 中'''
    # def name_list_to_string(l:list)->str:
    #     ans=''
    #     for i in l:
    #         ans=ans+', '
    with open(file_location, 'a+') as f:
        f.seek(0)
        content = f.readlines()
        # 如果之前有抽奖记录
        if content and content[0].strip():
            # 取出上一次的字符串
            last_lucky = content[-1][:-
                                     1].replace(' ', '').split(',')[-Lucky_Dog_Num:]
            print(f'上次中奖人员：{last_lucky}')
            crt_luck = Draw_Luckydog()
            # 如果有人又中奖了（看是否有交集）
            while set(crt_luck).intersection(set(last_lucky)):
                crt_luck = Draw_Luckydog()  # 再抽

        else:
            f.write(f"Time, LuckyDog 1, LuckyDog 2, LuckyDog 3, LuckyDog 4\n")
            crt_luck = crt_luck = Draw_Luckydog()
        print('本次中奖人员：', crt_luck)
        name_str = str(crt_luck)[1:-1].replace('\'', '')
        f.write(f"{Peking_Time()}, {name_str}\n")


def rowing_system():
    import_name_list()
    cal_probablity()
    query_and_save_in_csv(LuckyDogRecord)


if __name__ == '__main__':
    rowing_system()

# # 以下是随机性测试（共计10万次）
# dic = {k: 0 for k in name_list}  # 存储结果的字典为 0
# for i in range(1, 1000_000):
#     Lucky_Dog = random.choices(name_list, weights, k=Lucky_Dog_Num)
#     for j in Lucky_Dog:
#         dic[j] += 1


# for i in dic:
#     print(f'{i}: {dic[i]/1000_0}')
