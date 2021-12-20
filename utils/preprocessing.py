from typing import Tuple, Any, Type
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler


def normalize(data: pd.DataFrame, how: str = 'minmax') -> Tuple[pd.DataFrame, Any]:
    '''
    데이터 프레임의 데이터 중 "weeks" 열을 제외하고 정규화 합니다
    
    Args:
        data: "weeks"열을 포함하고 있는 데이터 프레임
        how: 정규화 방식 선택 "minmax" or "standard", default="minmax"
    
    Returns:
        정규화된 데이터 프레임과 스케일러를 반환합니다.
    '''
    
    # 정규화 방식 선택
    if how == 'minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    
    # weeks를 제외한 열 선택
    no_weeks_columns = [col for col in data.columns if col != 'weeks']
    scaler.fit(data[no_weeks_columns])
    norm = pd.DataFrame(scaler.transform(data[no_weeks_columns]),
                        columns=no_weeks_columns)
    
    # 첫 번째 열에 weeks를 삽입
    norm.insert(loc=0, column='weeks', value=data['weeks'])
    
    return norm, scaler
