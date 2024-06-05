import os
import pandas as pd
 
directory = r'data/csv'
 
header = {}
 
for filename in os.listdir(directory):
  if filename.endswith('.csv'):
    
    file_path = os.path.join(directory, filename)
    
    try:
      df = pd.read_csv(file_path, nrows=0 , encoding='UTF-8-sig')
      # df = pd.read_csv(file_path, encoding='euc-kr')
      header[filename] = df.columns.tolist()
    
      print(header)      
      # 1. 컬럼명 변환 (변환 기준은.. 파ㅇ명:std/컬럼명변환기준.csv)
    
    except Exception as e:
      print(f"Error reading {file_path}:{e}")

#변환된 컬럼명을 갖는 모든 파일을 읽어서 통합    
for i, (file, head) in enumerate(header.items()):
  
  #print(i, file, head)
  df_combined = pd.concat([pd.read_csv(os.path.join(directory, file) , encoding='UTF-8-sig') for file in header.keys()])

  df_combined = df_combined.loc[:, ~df_combined.columns.str.contains('^Unnamed')]
  
  df_combined.to_csv('./output/지자체빈집개방데이터통합.csv', index=True, encoding='UTF-8-sig')
    