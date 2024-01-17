# VJudge-Spider-on-TravisCI

![workflow](https://github.com/CUCCS/VJudge-Spider-on-TravisCI/actions/workflows/ci.yml/badge.svg)

> 此项目基于 `吕师哥` 开发的 `run.py`（关于 `run.py` 的 `说明文档` 见下文）。灵感来源于 `华睿师哥` 之前在此仓库使用的 `Action`

> Mr.Nobody 2022-10-16

## 目的

1. 实现比赛积分统计的 `定时全自动化` 执行
2. （可选）在更新完积分后，每场比赛 `自动抽奖`，并将结果存档记录至 `LuckyDogRecord.csv`

## 新学期使用前先

1. 根据本学期比赛的名称 `前缀` 修改 `get_url.py` 中的 `ContestPrefix` 变量（如 `'CUC-ACM-2022-Autumn-Training Round'`）；如果需要每次有比赛进行更新的时候进行 `加权抽奖`，请保证变量 `Draw` 为 `True`；否则为 `False`
2. 如果 `out.csv` 中还有上学期的记录，还是将数据存入至 `以往数据` 文件夹留存比较好
3. 清空 `out.csv`，`url.txt`，`LuckyDogRecord.csv`，`Weight.csv`（只清空里面的内容，不要删除文件本身）
4. 将 `ContestRecord.csv` 清空为下面的格式（记得第一行后有一个换行符，也就是说一共有两行）

```txt
name, begin_time, rank_url, ID, update_time

```

5. 设置定时执行

> 由于 `GitHub` 中的 `Schedule` 定时执行功能并非立即执行，而是开始排队——延迟可能高达一个多小时，甚至直接不执行。而比赛一般都在每周星期三 & 星期六下午 6：00 结束，我们需要一种 _准时执行_ 的方法。所以这里通过 `阿里云` 的 `函数计算（FC）` 功能 **定时** 向 `GitHub` 的 `API` 发送请求，通过 `GitHub` 的 `API` 触发 `workflows` 运行。实例是用的阿里云的 `函数计算` 功能来实现定时触发 `GitHub` 的 `API` （阿里云的配置方法详见 [运行不准时的解决办法](https://zhuanlan.zhihu.com/p/379365305)，其执行的函数为 `Ali_Triger.py`）

> 当然，如果不想部署阿里云的话就需要每次手动去 `Actions` 栏里面去 `Run workflow`

### 如果之前有多场比赛还没有更新

> 如果有多个比赛 `需要更新`，则会依次执行（所以如果一个学期之前都没有用此项目来记录积分也不要紧，只要比赛命名的前缀相同，该程序就会将所有的比赛 **依次** 更新完成）

## 关于抽奖

- 抽奖是一个加权抽奖。参与抽奖的同学为 `out.csv` 中排名前 `max_participants_num`（可以从 `LotteryMachine.py` 中修改此变量）
- 关于 `权重` —— 每次都会将参与抽奖的 `同学名字` 以及 `权重` 记录到 `Weight.csv` 中。目前的权重是根据此公式计算得出的（其实就是一个二次函数，$x$ 是积分排名）

$$
weight = 100 - \frac{x^2}{25}
$$

- 另外，上次中奖的同学第二次将不会中奖（不会连续中奖两次）
- 抽奖结果将会以 `csv` 文件的形式保存至 `LuckyDogRecord.csv` 中，作为 `日志`，也方便领奖

## 原理

1. 从 `Vjudege` 的 [比赛列表网页](https://vjudge.net/contest) 中 **根据前缀** 自动检索出本学期的 `比赛编号`，`开始时间` 等信息（所以一定要按照规范来命名比赛才行）
2. 根据 `ContestRecord.csv` 中的 `记录` 查询出 _已经被记录了的_ 比赛的 `比赛编号`
3. 下面两个条件 **都** 满足的即为需要更新的比赛
   - 比赛开始时间早于当前时间的比赛
   - `ContestRecord.csv` 还没有此比赛的记录
4. 启动 `run.py`，如果有多个比赛需要更新，则依次执行

# 下面是师哥写的关于 `run.py` 的说明文档

谁知道它能不能跑起来...

## Rank

https://github.com/CUCCS/VJudge-Spider-on-TravisCI/blob/main/out.csv

## 加分规则：

    总分 = 过题分 + 附加分 + 补题分(一周有效)+ 排名奖励分

    过题分:
    1分

    附加分
    Only AC: +1
    FB:      +0.5

    补题分
    solve_up:+0.5

    排名奖励分
    < 10%:   +4
    < 30%:   +3
    < 60%:   +2
    else :   +1

## Usage

**! 使用之前先**

```bash
git pull
```

1. 修改 `main` 分支下的 `url.txt` ，第一行写入本次训练网址，用于统计过题分数，第二行写入上次比赛网址,用于统计补题分数。注意输入链接是以`#rank`结尾的链接，不是比赛地址的链接! 如果上次或这次没有比赛，留空就行。
2. 写入完成后，将当前更改 push 到远程仓库 main 分支上。然后会在 Travis 上自动构建运行爬虫。
3. 等待片刻，在黄色圆点消失或喝杯咖啡之后,[点击上面的链接](https://github.com/CUCCS/VJudge-Spider-on-TravisCI/blob/main/out.csv)查看自动统计的结果。

## Attention

- **目前尚未在某个学期内实际测试过，可能有 bug。**

- 运行时确保 main 分支上有 out.csv 文件,且需要有 `out.csv` 中的标题行。

* 创建比赛时不要设置密码。

* 注意每手动 push 一次到 main 分支，都会构建一次，并且启动爬虫程序,更新上面链接中的积分。

### 标题行：

```
Name, Accepted, OnlyAC, FirstBlood, ThisRankScore, Upsolved, Score, SumScore, Rank
```

## Meet Error?

- 如果爬虫代码遇到问题，建议在本地运行,调试代码。需要的包在 `requirement.txt` 中。

### 本地运行：

### Linux

`.github/workflows/ci.yml` 中包含了需要的全部操作，不需要更改爬虫代码。

### Windows

#### Prerequisite

请自行下载 Chrome 浏览器 和 [Chromedriver](https://chromedriver.chromium.org/downloads),注意看网页上的版本选择说明。

#### 本地运行（建议提前做好备份）

```bash
git clone  https://github.com/CUCCS/VJudge-Spider-on-TravisCI.git
python run.py
```

#### 如果想要将本地更改推送上去而不触发构建：

在 commit 的 message 加上 `[skip ci]` 前缀。

参考链接：[Skipping workflow runs](https://docs.github.com/en/actions/managing-workflow-runs/skipping-workflow-runs)

## Acknowledgement

- [ididChan](https://github.com/ididChan) 关于 `.travis.yml` 提供的建议和图解

---

LyuLumos 2021.2.21

Maybe the last repo built for CUC-ACM Team
