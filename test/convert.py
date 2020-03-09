from zhconv import convert

def parse_content(content):
    content = content.replace(r'【.*?】', '')
    content = content.replace('\u3000', '')
    content = content.replace('\n', '')
    content = content.replace('\r', '')
    content = content.replace('\xa0', '')
    content = content.replace('-', '')
    content = content.replace('17173新闻采访部', '')
    content = content.replace(r'/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i', '')
    content = content.strip()
    content = convert(content, 'zh-cn')  # 将内容进行简繁体字转换

    return content

if __name__ == "__main__":
    print(parse_content("《蒼翼默示錄：神觀之夢》PC 版將於 4 月 26 日發售"))