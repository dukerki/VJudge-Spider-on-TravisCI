# VJudge-Spider-on-TravisCI
[![Build Status](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI.svg?branch=main)](https://www.travis-ci.com/LyuLumos/VJudge-Spider-on-TravisCI)

谁知道它能不能跑起来...

## Usage

修改`url.txt`，第一行为上次训练网址，用于统计补题分数，第二行为当前比赛网址。

## 碎碎念
（为什么StackOverflow上的解决方案都不适合俺呢...）

问：如何写.travis.yml文件？

答：去阿里云租一个免费的一小时的服务器，然后写shell，跑通了改成 yaml。

**PS：目前尚未在整个计分周期内测试过，可能有bug。**