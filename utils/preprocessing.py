from typing import Tuple, Any, Type
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler


def normalize_flu(data: pd.DataFrame, how: str = 'minmax') -> Tuple[pd.DataFrame, Any]:
    '''
    주/년도의 2차원으로 구성된 테이블 데이터를 정규화 합니다.
    
    매개변수 how를 사용해 정규화 방법을 지정할 수 있습니다.
    
    정규화된 데이터 테이블과 스케일러를 반환합니다.
    '''

    # 정규화 방법 선택
    if how == 'minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()

    # 전체 데이터에 대해 정규화하기 원하기 때문에 1차원으로 변경
    norm = pd.concat([srs for _, srs in data.items()], 
                     ignore_index=True)
    norm = norm.dropna().values.reshape(-1, 1)
    
    # 정규화 한 후, 다시 2차원으로 변경하여 같은 형태의 dataframe 생성
    scaler.fit(norm)
    norm = np.array(
        [scaler.transform(np.expand_dims(row, axis=1)).reshape(-1)
         for row in data.values])
    norm = pd.DataFrame(norm, 
                        columns=data.columns, 
                        index=data.index)
    
    # 53주 값이 비어 있을 경우 51주와 52주 값의 평균으로 채웁니다.
    for _, srs in data.items():
        # 빈 값이 1개이고 그것이 53주 인 경우 체크
        if srs.isna().sum() == 1 and np.isnan(srs[53]):
            srs[53] = np.mean([srs[51], srs[52]])
            
    return norm, scaler


def normalize_trends(data: pd.DataFrame, how: str = 'minmax') -> Tuple[pd.DataFrame, Any]:
    '''
    각 키워드의 
    '''
    if how == 'minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    
    no_weeks_columns = [col for col in data.columns if col != 'weeks']
    norm = pd.DataFrame(scaler.fit_transform(data[no_weeks_columns]),
                        columns=no_weeks_columns,
                        index=data.index)
    norm.insert(loc=0, column='weeks', value=data['weeks'])
    
    return norm, scaler
    
    
