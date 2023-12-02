import os
import pandas as pd

directory = 'Crawling\\Books_Data\\'  # 실제 경로로 변경해야 합니다.

df1 = pd.DataFrame()
df2 = pd.DataFrame()

# 해당 폴더 안의 파일 목록을 가져옵니다.
Topic_list = os.listdir(directory)

def is_csv_file(file_path):
    # 파일 이름에서 확장자 추출
    _, file_extension = os.path.splitext(file_path)
    
    # 확장자가 ".csv"인지 확인
    return file_extension.lower() == '.csv'

def make_path(path, name):
    return os.path.join(path + name) + '\\'

# 파일 목록을 출력합니다.
for Topic in Topic_list:
    print('-----> Topic :', Topic, '---------------------------------')
    folder_path = make_path(directory, Topic)
    folder_list = os.listdir(folder_path)

    for folderName in folder_list:
        # print(folderName)
        file_path = make_path(folder_path, folderName)
        file_list = os.listdir(file_path)
        for file in file_list:
            path = file_path + file
            print('-----> file :', file)
            if is_csv_file(file):
                data = pd.read_csv(path)
                data['Topic'] = Topic
                df1 = pd.concat([df1, data], ignore_index=True)
            else:
                review_list = os.listdir(path)
                for review in review_list:
                    review_data = pd.read_csv(path + '\\' + review)
                    df2 = pd.concat([df2, review_data], ignore_index=True)

df1.to_csv(directory + '\\' + 'books_data.csv')
df2.to_csv(directory + '\\' + 'review_data.csv')