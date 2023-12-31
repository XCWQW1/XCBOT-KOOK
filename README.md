<div align="center">
  
# XCBOT-KOOK

> 此版本已成为历史 新仓库：[kookbot2](https://github.com/XCWQW1/kookbot2)

一个萌新写的多线程+多进程的垃圾KOOK机器人框架

</div>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/static/v1?label=python&message=3.11.4&color=blue" alt="python">
  </a>
</P>
  
一个python萌新写的kook机器人屎山框架

<details>
<summary>开始使用：</summary>

- ### 1, 克隆本项目
  ```
  git clone https://github.com/XCWQW1/XCBOT-KOOK.git
  cd XCBOT-KOOK
  ```


- ### 2, 安装所需库

  ```pip install -r requirements.txt``` 

- ### 3, 创建或使用已有的KOOK机器人
  
  >请到[这里](https://developer.kookapp.cn/app/index)创建你的kook机器人

  创建好后在 应用>你创建的机器人>机器人>机器人连接模式 选择websocket
  复制你的TOKEN备用
- ### 4, 初始化
  请先执行```python main.py```初始化后再进行操作
  
- ### 4, 配置
  打开 config>config.ini 文件
  更改 token 为刚刚复制的 TOKEN
  
- ### 6, 编写插件 （可选）
	>示例的插件 kook_test.py、kook_http_api.py

- ### 7, 启动
  ```
  python main.py
  ``` 
	
  PS：第一次运行会停止2次初始化配置文件

</details>


有什么bug或者建议可以提Issues或者加入服务器后联系作者

官方服务器：[戳这里](https://kook.top/PDcaSp)

<details>
<summary>TODO：</summary>

  - #### 插件API
    - [x] 发送消息
    - [x] 引用消息
    - [x] 发送卡片
    - [x] 发送图片
    - [x] 上传文件
    - [x] 添加回应
    - [ ] 语音频道播放音乐
  
  - #### 框架API
    - [ ] onebot V11  （会做一些更改，比如send_group_msg会变成send_target_msg
    - [x] http api （只有一个发送消息的api也算是吧？后面慢慢完善
    - [ ] 正向ws
    - [ ] 反向ws
    - [ ] http post
</details>
