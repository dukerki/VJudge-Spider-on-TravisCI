#!/usr/bin/env bash

out="https://raw.githubusercontent.com/${USER}/${REPO}/blob/${TRAVIS_BRANCH}/out.csv"

wget -O ../${FILES}  "$out" 

file1="out.csv"
file2="../out.csv"

if cmp -s "$file1" "$file2"; then
    echo "成功,远程仓库上out.csv文件已更改" 
else 
    echo "ERROR:远程仓库上文件未更改,上传仓库失败。可能github token已失效，需要在设置中同名替换新的有效token"
    exit 1;
fi
