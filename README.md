# VJudge-Spider-on-TravisCI
[![Build Status](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI.svg?branch=data)](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI)

谁知道它能不能跑起来...

## Ranking File Link

https://github.com/LyuLumos/VJudge-Spider-on-TravisCI/blob/main/out.csv

## Usage

1. 修改 `main` 分支下的 `url.txt` ，第一行为上次训练网址，用于统计补题分数，第二行为当前比赛网址。
2. 从 `main` 分支向 `data` 分支发起PR，合并后 Travis 将自动执行。

如果需要做出修改 `out.csv`  内容请在 `main` 分支上进行增删。

## Attention

- **目前尚未在某个学期内实际测试过，可能有bug。**
- 单学期内首末两次计分如遇到爬虫代码问题请手动调整 `run.py`。
- 首次运行请保留 `out.csv` 中的标题行。



## Meet Error?

如果爬虫代码遇到问题，建议在本地运行。需要的包在 `requirement.txt` 中。

### Linux


`.travis.yml` 中包含了需要的全部操作，不需要更改爬虫代码。

### Windows

请自行下载 Chrome浏览器 和 Chromedriver，注释 `run.py` 74-79行，取消注释第80行，之后再运行。

# 本地运行（建议提前做好备份）
python run.py
```


## Acknowledgement

- [ididChan](https://github.com/ididChan) 关于 `.travis.yml` 提供的建议和图解

---

LyuLumos 2021.2.21

Maybe the last repo built for CUC-ACM Team