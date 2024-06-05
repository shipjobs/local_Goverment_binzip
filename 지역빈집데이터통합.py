import os
from time import sleep
import pandas as pd
import csv


directory = r'data/csv'
#변환 기준 파일 읽기 ("std/컬럼명변환기준.csv")
df = pd.read_csv('std/컬럼명변환기준.csv', encoding='utf-8')
values_asis = df.iloc[:, 0].tolist()  #각 지자체에서 사용하는 컬럼명 리스트
values_tobe = df.iloc[:, 1].tolist()  #통합할 컬럼명 리스트 (사용안함으로 표기된 컬럼은 제외, Unnamed 으로 표기됨)

#전체 파일대상
for filename in os.listdir(directory):
  if filename.endswith('.csv'):
    file_path = os.path.join(directory, filename)

    data = pd.read_csv(file_path, encoding='utf-8')
    matching_columns = [col for col in data.columns if col in values_asis]    
    
    for col in matching_columns:
      
      if 'Unnamed' in col:
        data.rename(columns={col: '사용안함'}, inplace=True)
      else:
        data.rename(columns={col: values_tobe[values_asis.index(col)]}, inplace=True)        
      
    #변경된 컬럼명으로 파일 저장    
    data.to_csv(file_path, index=False, encoding='utf-8')  
    sleep(1)  #파일 저장시간을 위해 1초 대기
     
    

#변경된 컬럼 정보기준, 전체 파일을 읽어서 하나의 파일로 통합    
header = {}
 
for filename in os.listdir(directory):
  if filename.endswith('.csv'):
    
    file_path = os.path.join(directory, filename)
    
    try:
      df = pd.read_csv(file_path, nrows=0 , encoding='UTF-8-sig')
      header[filename] = df.columns.tolist()
      #print(header)      
    
    except Exception as e:
      print(f"Error reading {file_path}:{e}")

#변환된 컬럼명을 갖는 모든 파일을 읽어서 통합 (동일 컬럼명끼리 값도 통합 되도록 함, 값이 없는 경우 Unnamed 으로 표기됨)   
for i, (file, head) in enumerate(header.items()): 
  #print(i, file, head)
  df_combined = pd.concat([pd.read_csv(os.path.join(directory, file) , encoding='UTF-8-sig') for file in header.keys()])

  df_combined = df_combined.loc[:, ~df_combined.columns.str.contains('^Unnamed')]
  
  #DB에 지지체별로 저장할 경우, 지자체명 (파일명) 컬럼 추가
  df_combined.insert(0, '지자체명', file)
  df_combined.to_csv('./output/지자체빈집개방데이터통합.csv', index=True, encoding='UTF-8-sig')
  sleep(1)  #파일 저장시간을 위해 1초 대기
    