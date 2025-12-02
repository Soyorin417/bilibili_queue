# blivedm-queue

本项目继承[blivedm](https://github.com/xfgryujk/blivedm)

## blivedm介绍

Python获取bilibili直播弹幕的库，使用WebSocket协议，支持web端和B站直播开放平台两种接口

[协议解释](https://open-live.bilibili.com/document/657d8e34-f926-a133-16c0-300c1afc6e6b)

基于本库开发的一个应用：[blivechat](https://github.com/xfgryujk/blivechat)

### 使用说明

1. 需要Python 3.8及以上版本
2. 安装依赖

    ```sh
    pip install -r requirements.txt
    ```

3. web端例程在[sample.py](./sample.py)，B站直播开放平台例程在[open_live_sample.py](./open_live_sample.py)

## blivedm-queue介绍

本项目采用vue前端，Flask 后端

初次使用点击```start_all.bat```弹出三个黑窗口先别关(有一个乱码可以关)

访问http://localhost:8080/

<img width="887" height="509" alt="image" src="https://github.com/user-attachments/assets/3e85a7b6-224c-4a2f-ad75-d07992fd1e42" />

