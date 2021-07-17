# VJudge-Spider-on-TravisCI
[![Build Status](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI.svg?branch=data)](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI)

谁知道它能不能跑起来...

## Ranking File Link

https://github.com/LyuLumos/VJudge-Spider-on-TravisCI/blob/out/out.csv

## 加分规则：
    总分 = 过题分 + 附加分 + 补题分(一周有效)+ 排名奖励分

    过题分:
    1分

    附加分
    Only AC: +0.5
    FB:      +0.2   

    补题分
    solve_up:+0.5

    排名奖励分
    < 10%:   +4
    < 30%:   +3
    < 60%:   +2
    else :   +1
 
## Usage

1. 修改 `main` 分支下的 `url.txt` ，第一行写入本次训练网址，用于统计补题分数，第二行写入上次比赛网址。如果没有，空行就行。
2. 写入完成后，将当前更改push 到远程仓库main分支上。然后会在Travis上自动运行。
3. 最后点击上面的链接查看结果。
如果需要做出修改 `out.csv`  内容请在 `out` 分支上进行增删。

## Attention

- **目前尚未在某个学期内实际测试过，可能有bug。**
- 单学期内首末两次计分如遇到爬虫代码问题请手动调整 `run.py`。
- 运行时确保out分支上有out.csv文件,且需要有 `out.csv` 中的标题行。
* 创建比赛时不要设置密码。
* 每push一次到main分支，都会启动爬虫程序！
```
Name, Accepted, OnlyAC, FirstBlood, ThisRankScore, Upsolved, Score, SumScore, Rank
```

## Meet Error?

如果爬虫代码遇到问题，建议在本地运行,调试代码。需要的包在 `requirement.txt` 中。
### 本地运行：
### Linux

`.travis.yml` 中包含了需要的全部操作，不需要更改爬虫代码。

### Windows

请自行下载 Chrome浏览器 和 Chromedriver，注释 `run.py` 74-79行，取消注释第80行，之后再运行。

#### 本地运行（建议提前做好备份）
```bash
git clone --branch=out https://github.com/LyuLumos/VJudge-Spider-on-TravisCI.git
python run.py
```
之后进入`VJudge-Spider-on-TravisCI` 子文件的out.csv文件查看结果。
#### 如果想要将运行结果推送上去：
确保在VJudge-Spider-on-TravisCI目录下。
```bash
git commit -a
git push orgin out
```

##### 
## Acknowledgement

- [ididChan](https://github.com/ididChan) 关于 `.travis.yml` 提供的建议和图解

---

LyuLumos 2021.2.21

Maybe the last repo built for CUC-ACM Team

