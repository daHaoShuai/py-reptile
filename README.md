# py-reptile
自己学习爬虫的一些记录

## 爬取桂林理工大学南宁分校个人课程安排信息
思路: 解析http://jw.glutnn.cn/academic/student/currcourse/currcourse.jsdo的内容,保存需要的信息到csv文件中
获取登陆后的cookie
![登陆后的cookie](./imgs/%E8%8E%B7%E5%8F%96cookie.png)

```python
# 需要cookie才能有权限访问页面
get_course_info('JSESSIONID=6204F1171AB46F49E94D50ECD988FCE7.TA2')
```