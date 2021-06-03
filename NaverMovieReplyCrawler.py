#step 0. 필요 모듈 라이브러리 로딩, 검색어 입력
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import urllib
import datetime
import time
import sys
import os

query_txt = '엔드게임'##input('1. 크롤링할 키워드는 무엇입니까? : ')
post_EA = int(100)##(input('2. 크롤링 할 리뷰건수는 몇건입니까?')
f_dir = 'E:/coding/3years/python/W14'##input("3. 파일을 저장할 위치를 입력하십시오. : ")


now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


os.chdir(f_dir)
f_dir += "" if f_dir[-1:] == "/" else "/"
os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)
f_result_dir = f_dir+s+'-'+query_txt

try:
  #step 1. 크롬 드라이버 사용, 웹 브라우저 실행
  path = "E:/coding/3years/chrome driver/chromedriver.exe"
  driver = webdriver.Chrome(path)

  url = "https://movie.naver.com/"
  driver.get(url)
  time.sleep(2)


  #키워드 검색
  search = driver.find_element_by_id('ipt_tx_srch')
  search.send_keys(query_txt)

  #검색 버튼 누름
  driver.find_element_by_class_name('btn_srch').click()

  #로딩된 HTML 가져오기
  time.sleep(2)
  full_html = driver.page_source
  soup = BeautifulSoup(full_html, 'html.parser')

  #검색 결과가 있는지 확인
  try:
    content_list = soup.find("ul", class_="search_list_1").find_all("li")

    targetIndex = 0
    #검색 결과 다수
    if len(content_list) > 1:
      print("검색 결과가 두개 이상입니다. 평가 참여 인원이 높은 영화의 결과를 추출합니다.")
      cuser_cnt = 0
      
      for i in range(0, len(content_list)):
        try:
          cur_cuser_cnt =  int(content_list[i].find("em", class_="cuser_cnt").get_text()[4:-2])
          if cuser_cnt < cur_cuser_cnt:
            cuser_cnt = cur_cuser_cnt
            targetIndex = i
          break;
        except:
          continue
        
    driver.get(url + content_list[targetIndex].find('a')['href'][1:])

  
      
  #검색 결과 없음
  except:
    print("검색 결과가 없거나 오류가 발생하였습니다.")
    driver.quit()
  
  #로딩된 HTML 가져오기
  time.sleep(2)

  driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/a').click()
  

    
  #페이지 카운터
  page = 1

  #크롤링 시작
  reply = 1
  index = []
  score = []
  content = []
  author = []
  date = []
  like = []
  dislike = []

  while True:
    #로딩된 HTML 가져오기
    time.sleep(2)
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')  

    content_list = soup.find('div', class_='score_result').find('ul').find_all('li')
    print(content_list)

    for i in range(0, len(content_list)):
      index.append(reply)
      print(str(reply), '번째 리뷰입니다.', '='*20)
      reply += 1
      
      gscore = content_list[i].find('div', class_='star_score').find('em').get_text().strip()
      print('1.별점 :', gscore)
      score.append(gscore)

      gcontent = content_list[i].find('div', class_='score_reple').find('span', id='_filtered_ment_0').get_text().strip()
      print('2. 리뷰내용 :', gcontent)
      gcontent
    



##    if reply == post_EA:
##      break
##    else:
##      driver.find_element_by_xpath('//*[@id="pagerTagAnchor" + page]').click()

##except:
##  print("오류가 발생했습니다.")
finally:
  driver.quit()

