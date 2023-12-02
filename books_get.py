from crawling_Books_Reviews import crawlingStart


# 
# https://product.kyobobook.co.kr/category/KOR/19#?type=home // 역사/문화
# https://product.kyobobook.co.kr/category/KOR/03#?type=home // 시/에세이
# https://product.kyobobook.co.kr/category/KOR/05#?type=home // 인문

urlList = [
    # 'https://product.kyobobook.co.kr/category/KOR/0101#?page=1&type=all&sort=new', # 소설
    # 'https://product.kyobobook.co.kr/category/KOR/19#?type=home', # 역사/문화
    # 'https://product.kyobobook.co.kr/category/KOR/03#?type=home', # 시/에세이
    # 'https://product.kyobobook.co.kr/category/KOR/05#?type=home', # 인문
    'https://product.kyobobook.co.kr/category/KOR/07#?type=home', # 가정/육아
    'https://product.kyobobook.co.kr/category/KOR/08#?type=home', # 요리
    'https://product.kyobobook.co.kr/category/KOR/09#?type=home', # 건강
    'https://product.kyobobook.co.kr/category/KOR/11#?type=home', # 취미/실용/스포츠
    # 'https://product.kyobobook.co.kr/category/KOR/13#?type=home', # 경제/경영 // 바꿔야 될 것들이 많아서 취소
    'https://product.kyobobook.co.kr/category/KOR/15#?type=home', # 자기계발
    'https://product.kyobobook.co.kr/category/KOR/17#?type=home', # 정치/사회
    'https://product.kyobobook.co.kr/category/KOR/21#?type=home', # 종교
    'https://product.kyobobook.co.kr/category/KOR/23#?type=home', # 예술/대중문화
    'https://product.kyobobook.co.kr/category/KOR/25#?type=home', # 중/고등 참고서 // 8
    'https://product.kyobobook.co.kr/category/KOR/26#?type=home', # 기술/공학
    'https://product.kyobobook.co.kr/category/KOR/27#?type=home', # 외국어 // 10
    'https://product.kyobobook.co.kr/category/KOR/29#?type=home', # 과학이론
    'https://product.kyobobook.co.kr/category/KOR/59#?page=1&type=all&sort=new', # 교보 오리지널
    'https://product.kyobobook.co.kr/category/KOR/31#?type=home', # 취업/수험서
    'https://product.kyobobook.co.kr/category/KOR/32#?type=home', # 여행
    'https://product.kyobobook.co.kr/category/KOR/33#?type=home', # 컴퓨터/IT // 15
    'https://product.kyobobook.co.kr/category/KOR/35#?type=home', # 잡지
    'https://product.kyobobook.co.kr/category/KOR/38#?type=home', # 청소년
    'https://product.kyobobook.co.kr/category/KOR/39#?type=home', # 초등참고서
    'https://product.kyobobook.co.kr/category/KOR/41#?type=home', # 유아
    'https://product.kyobobook.co.kr/category/KOR/42#?type=home', # 어린이 // 20
    'https://product.kyobobook.co.kr/category/KOR/47#?type=home', # 만화
    'https://product.kyobobook.co.kr/category/KOR/53#?type=home', # 한국소개도서
    'https://product.kyobobook.co.kr/category/KOR/50#?page=1&type=all&sort=new' # 대학교재 // 23
]
directory_path = 'C:\\Users\\inbn1\\Documents\\Programers\\Crawling\\books'

# url = "https://product.kyobobook.co.kr/category/KOR/19#?type=home"

urlNum = 19
cateNum = 0
for i in range(urlNum, len(urlList)):
    crawlingStart(urlList[i], directory_path, i, cateNum)

