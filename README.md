# Xinshou - 心手

## 开源说明

使用flask开发，一个入门级的项目。  
目前用于我的微信公众号。

代码结构如下：

1. db: 持久化层 使用MongoDB.
2. model: 路由模块.
3. processor: 相当于controller层.
4. static: 静态文件目录.
5. templates: 网页模板(Jinja2).
6. utils: 工具包.
7. views: 用于后台的视图层.
8. wx: 微信格式封装

感谢ws和cw两位大佬的帮助。

## 使用说明

配置好MongoDB.  
根据config-example.py完善config.py  
运行shell/run.sh即可.

## 免责说明

代码仅供研究与学习交流之用  
另外鄙视一下利用信息差牟利的同学
