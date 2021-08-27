import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import schedule
import time
import json
import ssl

def setNew(): # 가장 최근 회차 번호 업데이트
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    url = 'https://dhlottery.co.kr/gameResult.do?method=byWin&wiselog=H_C_1_1'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    text = ""

    for meta in soup.head.find_all('meta'):
        text += str(meta.get('content'))
        text += '\n'

    index = 0
    numbers = []
    flag = False

    for x in text:
        if x >= '0'and x <= '9':
            if flag == False:
                numbers.append("")
            numbers[index] += str(x)
            flag = True
        else:
            if flag == True: 
                index += 1
                flag = False

    return int(numbers[0]) # 가장 최근 회차 번호
    # numbers index 별 정보
    # 0 : 회차
    # 1 ~ 6 : 당첨 번호
    # 7 : 보너스 번호
    # 9 : 1등 당첨 인원 수
    # 11 ~ end : 1등 1인당 당첨 금액

def setData(): # 토요일 오후 10시마다 호출
    global jsonText
    jsonText = "{\n"

    new = setNew() + 1 # 가장 최근 회차 + 1, 다음에 받아올 회차
    old = new - 53  # 가장 최근 회차 - 52

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    for i in range(old, new): # 925회부터 977회까지
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)
        result = urlopen(url).read()
        lotto = json.loads(result)

        text = ""
        text = "\t\"%d\":{\n" %i + str(lotto) + "\n\t},\n"
        jsonText += text

    jsonText += "\n}"
    # f = open("/Users/orijoon98/Desktop/GitHub/LottoRestApi/lotto.txt", 'w')
    f = open("/home/pi/Lotto/lotto.txt", 'w')
    f.write(jsonText)
    f.close()
    print("call") 

schedule.every(5).seconds.do(setData)
schedule.every().saturday.at("22:00").do(setData)

while True:
    schedule.run_pending()
    time.sleep(1)
