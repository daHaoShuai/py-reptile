import requests
from lxml import etree


def get_course_info(cookie: str) -> None:
    """
    获取个人课程安排表信息
    """
    # 课程安排
    url = 'http://jw.glutnn.cn/academic/student/currcourse/currcourse.jsdo'

    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)

    html = etree.HTML(response.text)

    # 第一个table标签
    table = html.xpath('//table[@class="infolist_tab"]')[0]
    # 解析第一层的tr标签
    trs = table.xpath('./tr[@class="infolist_common"]')
    result = []  # 保存解析结果
    for tr in trs:
        tds = tr.xpath('./td')
        row = []  # 保存一行的信息
        for td in tds:
            # 去除空格和回车
            info_one = td.xpath('./text()')[0].strip().replace('\n', '')
            if not info_one == '':
                row.append(info_one)
            info_two = td.xpath('./a/text()')
            if len(info_two) > 0:
                row.append(info_two[0].strip().replace('\n', ''))
            info_three = [s.xpath('./text()')
                          for s in td.xpath('./table/tr/td')]
            if len(info_three) > 0:
                tmp = [(s[0]).strip().replace('\n', '') for s in info_three]
                row.append(tmp)
        result.append(row)

    # 写入csv文件中
    with open('课程安排.csv', 'w', encoding='utf-8') as f:
        # 写入第一行
        f.write('课程号,序号,课程名称,任课教师,学分,选课属性,考核方式,考试性质,是否缓考,上课时间、地点\n')
        for row in result:
            if '任选' in row:
                row[3], row[4] = row[4], row[3]
                row.append('')
            line = ','.join(row[:-1])+','+'、'.join(row[-1]) + '\n'
            f.write(line)
    print('保存课程安排信息到了 "课程安排.csv" 中')


if __name__ == '__main__':
    # http://jw.glutnn.cn/academic/common/security/login.jsp 登录
    # http://jw.glutnn.cn/academic/student/currcourse/currcourse.jsdo 获取 Cookie
    get_course_info('JSESSIONID=6204F1171AB46F49E94D50ECD988FCE7.TA2')
