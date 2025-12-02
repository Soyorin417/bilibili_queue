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



保存配置





#### 管理界面

<img width="1892" height="469" alt="image" src="https://github.com/user-attachments/assets/dd0b40bb-23fc-4acf-bd5a-6101fbb5c1b0" />

这个看情况自己生成背景，默认也可以点击生成后，点击复制，会跳确认弹窗



<img width="1905" height="930" alt="image" src="https://github.com/user-attachments/assets/029786ce-b5c6-4329-ab6d-dad065a7a381" />



```!!!一定要把这个确认点了```

<img width="1014" height="351" alt="image" src="https://github.com/user-attachments/assets/78f69c88-e8bd-4704-9447-106b3f097e90" />



此时你的剪贴版会有css格式，打开obs新建立浏览器源

<img width="611" height="389" alt="image" src="https://github.com/user-attachments/assets/83d4f299-28de-4151-b67b-c6ae31514bb9" />

把本地文件勾上，选择queue.html

<img width="1540" height="630" alt="image" src="https://github.com/user-attachments/assets/645d6e81-ebd2-4e71-bc55-b3a68cd2b495" />

划到下面把css复制黏贴好
要是想改关键词，这里修改

<img width="1884" height="633" alt="image" src="https://github.com/user-attachments/assets/b7f7bde4-f2f2-4f77-88ee-d4aae01e5780" />

都结束可以直接关掉三个窗口

在这打开终端 

<img width="965" height="510" alt="image" src="https://github.com/user-attachments/assets/0d4d48cd-f499-48dc-ba2e-6cd3f5847da8" />
输入```python .\sample.py```

就可以监听直播了

手动操作还是打开```start_all.bat```入队出队

