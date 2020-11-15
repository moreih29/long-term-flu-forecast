# Multi-encoding based influenza outbreak forecast in the distant future using time-delay of web data

### Intoduction
인플루엔자는 매년 290,000 - 650,000명의 사망자를 발생시키는 위협적인 감염병이다. 미국은 Center for Disease Control and Prevent (CDC), 유럽은 the European influenza Surveillance Scheme (EISS), 한국은 the Korean Centers for Disease Control
and Prevention (KCDC)를 통해 인플루엔자의 발생을 감시하고 있다. 그러나, 이런 전통적인 통계 기반 감시 방법은 사람들에게 정보가 제공되기까지 1-2주의 시간이 지연된다. 이 문제를 해결하기 위해 news, SNS, search query 등을 사용하여 인플루엔자 발생을 예측하는 연구들이 진행되어 왔다. 
대부분의 기존 연구들은 1-2주의 단기간 예측 문제에 집중하고 있다. 효과적인 인플루엔자 예방을 위해서는 5주 이상의 장기간 예측이 반드시 필요하지만, 장기간 예측은 예측 기간이 늘어남에 따라 예측의 오류가 누적되어 정확도가 크게 하락하는 문제를 갖는다. 이 문제를 해결하기 위해서 누적되는 예측의 오류를 보정할 유의미한 데이터를 찾는 것이 필수적이다.

<img src="./image/v2/US_delay_example(colds).png" width="50%"/>

위 그림은 미국의 인플루엔자 의사 환자 분율(influenza like illness, ILI)과 구글 검색 엔진에서 "colds"의 검색 비율, 그리고 그 비율을 6주 평행 이동 시킨 것을 보여준다. 이 처럼, 특정 웹 데이터는 ILI 와 시간 지연된 상관 관계를 가질 수 있으며 웹 데이터의 시간 지연된 부분은 미래 인플루엔자 예측을 위한 지표로 사용될 수 있다.
본 논문은 과거의 ILI 데이터와 시간 지연된 웹 데이터를 사용하여 장기간 인플루엔자를 예측하기 위해 웹 데이터의 시간 지연을 사용한 다중 인코딩 기반 인플루엔자 예측 모델을 제안한다.
본 논문의 핵심은 다음과 같다.
- 본 논문은 웹 데이터의 시간 지연성을 사용하여 높은 정확도를 갖는 장기간 인플루엔자 예측 방법을 제안한다.
- 제안된 모델의 다중 인코더는 웹 데이터 수집의 어려움에 따른 불충분한 학습량을 보완한다. 
- 본 논문은 인플루엔자 예측에 적합한 웹 데이터를 찾고 제안된 방법을 다양한 국가에 적용했다.
- 제안된 방법은 5주 이상의 장기간 예측에서 다른 최신 방법보다 더 높은 성능을 달성했다.

### Method
<img src="./image/v2/model_structure.png" />