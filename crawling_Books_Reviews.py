# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import json

import pandas as pd
import numpy as np

# BeautifulSoup 패키지 불러오기
from bs4 import BeautifulSoup as bs

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

import os

def crawlingStart(url, directory_path, num, cateNum):


    # 크롬드라이버 실행
    driver = webdriver.Chrome() 

    # 화면 크기 설정
    driver.set_window_size(1920, 1080)

    #크롬 드라이버에 url 주소 넣고 실행
    driver.get(url)

    html = driver.page_source
    soup = bs(html, 'html.parser')

    name = soup.select('#contents > div > aside > div.aside_body > div.snb_wrap > a')[0].text.replace('/', '·')

    directory_path += '\\' + name

    os.makedirs(directory_path, exist_ok=True)

    categories = soup.select('#contents > div > aside > div.aside_body > div.snb_wrap > ul > li > a')

    wait = WebDriverWait(driver, 5)

    for i in range(cateNum, len(categories)):
        start = time.time()

        print("----->" + ' category : ' +str(i))
        cateUrl = categories[i].get('href')

        driver.get(cateUrl)

        time.sleep(2)
        # btn1 = driver.find_element(By.ID, 'allSort-button')
        try:
            btn1 = wait.until(EC.presence_of_all_elements_located((By.ID, 'allSort-button')))
            btn1[0].click() 

            time.sleep(2)
            sales_rates = driver.find_elements(By.XPATH, '//*[@id="allSort-menu"]/li/div')
            # sales_rates = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            sales_rates[1].click() 
        except:
            pass

        time.sleep(2)
        # btn2 = driver.find_element(By.ID, 'allPer-button')
        #bestPer-button
        try:
            btn2 = wait.until(EC.presence_of_all_elements_located((By.ID, 'allPer-button')))
        except:
            btn2 = wait.until(EC.presence_of_all_elements_located((By.ID, 'bestPer-button')))
        btn2[0].click() 

        time.sleep(2)
        try:
            amounts = driver.find_elements(By.XPATH, '//*[@id="allPer-menu"]/li/div')
            amounts[1].click() 
        except:
            amounts = driver.find_elements(By.ID, 'ui-id-42')
            amounts[0].click()
        # amounts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
        #ui-id-42

        time.sleep(4)

        html = driver.page_source
        soup = bs(html, 'html.parser')

        books = soup.select('#homeTabAll > div.switch_prod_wrap.view_type_list > ol > li > div.prod_area.horizontal > div.prod_info_box > a')
        cnt2 = 0

        df = pd.DataFrame(columns=['title', 'author', 'intro', 'publisher', 'publication_date', 'isbn', 'genre', 'category', 'images'])

        review_df = pd.DataFrame(columns=['isbn', 'user_id', 'reg_date', 'contents', 'rating'])


        for j in range(len(books)):

            bookUrl = books[j].get('href')

            checkNum = bookUrl.split('/')[-1]

            driver.get(bookUrl)

            adult_url = f'https://mmbr.kyobobook.co.kr/login?continue=http%3A%2F%2Fproduct.kyobobook.co.kr%2Fdetail%2F{checkNum}&verify=adult'

            if driver.current_url == adult_url:
                continue


            # bs4 세팅
            html = driver.page_source
            soup = bs(html, 'html.parser')
            #contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span


            ##### TITLE

            source_title = soup.select('#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1')

            count = 0
            while len(source_title) <= 0:
                if count >= 10:
                    break
                time.sleep(2)
                source_title = soup.select('#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1')
                count += 1

            title = source_title[0].text
            title = title.replace("\n", '').replace('/', '·')
            ##### TITLE
            print("----->" + title + ' : ' +str(j+1) + ', category : ' + str(i) + ', urlNum : ' + str(num))

            ##### CATEGORY
            source_category = soup.select('#mainDiv > main > section.breadcrumb_wrap > div > ol > li:nth-child(5) > a')

            if source_category:
                category = source_category[0].text.replace("/", '·')
            else:
                category = None
            ##### CATEGORY

            ##### ISBN
            source_isbn = soup.select('#scrollSpyProdInfo div.tbl_row_wrap table tbody tr:nth-child(1) td')
            if source_isbn:
                print('-----> ISBN True')
            else:
                source_isbn = soup.select('#contents > div > div.header_contents_inner > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > dl > dd:nth-child(3) > em')
                print('-----> ISBN False')

                # if not source_isbn:
                #     source_isbn = soup.select('#scrollSpyProdInfo > div.tbl_row_wrap > table > tbody > tr:nth-child(1) > td')
                #     print('-----> ISBN False2')
        #scrollSpyProdInfo > font > div.product_detail_area.basic_info > div.tbl_row_wrap > table > tbody > tr:nth-child(1) > td
    # common_path = '#scrollSpyProdInfo > div.product_detail_area.basic_info > div.tbl_row_wrap > table > tbody > tr:nth-child(1) > td'
    #scrollSpyProdInfo > div.product_detail_area.basic_info > div.tbl_row_wrap > table > tbody > tr:nth-child(1) > td
            if source_isbn:
                isbn = source_isbn[0].text
            else:
                isbn = None
            ##### ISBN



            custom_header = {
                'referer' : f'{bookUrl}',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0' 
            }
            dataUrl = f'https://product.kyobobook.co.kr/api/review/list?page=1&pageLimit=100000&reviewSort=001&revwPatrCode=000&saleCmdtid={checkNum}'
            print('-----> dattUrl : ',dataUrl)

            parsed_data = {}

            req = requests.get(dataUrl, headers=custom_header)

            if req.status_code == requests.codes.ok:
                count = 0
                while True:
                    if count >= 5:
                        break
                    try:
                        parsed_data = json.loads(req.text)
                        break
                    except:
                        count += 1
                        time.sleep(2)

            if not parsed_data:
                continue
            reivew_length = len(parsed_data['data']['reviewList'])


            for r in range(reivew_length):
                user_id = parsed_data['data']['reviewList'][r]['mmbrId']
                reg_date = parsed_data['data']['reviewList'][r]['cretDttm']
                contents = parsed_data['data']['reviewList'][r]['revwCntt'].replace('&nbsp;', ' ').replace('\r\n', '').replace('&#30059;', '你')
                rating = parsed_data['data']['reviewList'][r]['revwRvgr']

                review_data_to_append = pd.DataFrame({
                'isbn' : [isbn],
                'user_id' : [user_id],
                'reg_date' : [reg_date],
                'contents' : [contents],
                'rating' : [rating]
                })

                review_df = pd.concat([review_df, review_data_to_append], ignore_index=True)

            ##### AUTHOR
            source_author = driver.find_element(By.CLASS_NAME, 'author')

            source_author = soup.select('#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_author_box.auto_overflow_wrap > div.auto_overflow_contents > div > div')

            source_author_checked = source_author[0].text.replace("\n", '').split(',')

            author = [i.strip().replace(' ', '') for i in source_author_checked]
            ##### AUTHOR
            
            ##### INTRO
            source_intro = soup.select('#scrollSpyProdInfo > div.product_detail_area.book_intro > div.intro_bottom > div')
            
            if source_intro:
                print('-----> INTRO True')
                if len(source_intro) > 1:
                    intro = source_intro[0].text + '\n' + source_intro[1].text
                    intro = intro.split('\n')
                else:
                    source_intro = source_intro[0]
                    intro = source_intro.text
                    intro = [intro]
            else:
                source_intro = soup.select('#bookIntc > div.auto_overflow_contents > div > div')
                print('-----> INTRO False')

                if not source_intro:
                    print('-----> INTRO False2')
                    source_intro = soup.select('#scrollSpyProdInfo > div.product_detail_area.book_inside > div.auto_overflow_wrap.type_text.overflow > div.auto_overflow_contents > div > p')

                if not source_intro:
                    print('-----> INTRO False3')
                    intro = [None];
                else:
                    intro = source_intro[0].text
                    intro = [intro]
            ##### INTRO


            ##### IMAGE
            source_images = soup.select('div.blur_img_box img')

            images = [i['data-src'] for i in source_images]
            ##### IMAGE

            ##### PUBLISHER
            publisher = soup.select('#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date > a')

            if publisher:
                print('-----> PUB True')

                publisher = publisher[0].text

                source = soup.select('#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date')

                source_pub = source[0].text.replace('\n', '').replace(' ', '').split('·')

                publication_date = source_pub[1].split('(')[0]
            else:
                print('-----> PUB False')
                publisher = soup.select('#contents > div > div.header_contents_inner > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date > i')[0].text
                publication_date = soup.select('#contents > div > div.header_contents_inner > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_info_text.publish_date > p:nth-child(2)')[0].text.replace('\n', '').replace(' ', '')
            ##### PUBLISHER

            ##### GENRE
            source_genre = soup.select('#mainDiv > main > section.breadcrumb_wrap > div > ol > li:nth-child(4) > a')

            genre = source_genre[0].text
            ##### GENRE


            ##### 데이터 프레임 생성
            data_to_append = pd.DataFrame({
                'title' : title,
                'author' : [author],
                'intro' : [intro],
                'publisher' : publisher,
                'publication_date' : publication_date,
                'isbn' : isbn,
                'genre' : genre,
                'category' : category,
                'images' : [images]
            })

            print(data_to_append['isbn'])

            ##### 데이터 프레임 합치기
            df = pd.concat([df, data_to_append], ignore_index=True)

            time.sleep(1)
            print("Crawling Success!!!!!!!!!!!!!! : ", title)

        end = time.time()

        print("-----> 카테고리 크롤링 시간 : " +  str(end-start))
        
        
        ##### books 저장
        category_path = directory_path + '\\' + str(category)
        os.makedirs(category_path, exist_ok=True)
        books_file_path = category_path + '\\'+ str(category) + '.csv'
        df.to_csv(books_file_path)


        #### review 저장
        review_path = directory_path + '\\' + str(category) + '\\' +'reviewFiles'
        os.makedirs(review_path, exist_ok=True)
        review_file_path = review_path + '\\' + 'review.csv'
        review_df.to_csv(review_file_path)
        
    if cateNum:
        cateNum = 0