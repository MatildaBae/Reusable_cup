# ♻️ Location Selection for Reusable Cup Return Stations in Seoul & Service Optimization

**2024 5th Data Analysis for Business (DAB) Competition, Korea University**
*3th Place - November 2024*

**Team Dolrido**  
*Members: Kim Na-yeon (Statistics), Kim Ye-eun (Statistics), Bae Ji-won (Economics), Jeong Ha-yeon (Business), Choi Joo-hee (Media Studies)*  

## 🚀 Overview

This project focuses on selecting optimal locations for reusable cup return stations in Seoul using the **Maximum Covering Location Problem (MCLP)** algorithm, while analyzing the profitability of operating a reusable cup return service under a deposit refund system. The goal is to reduce single-use plastic waste, contribute to environmental sustainability, and support the adoption of reusable cups in Seoul.

---

## 💡 Project Objectives

1. **MCLP Algorithm Application**: To maximize the coverage of demand points (cafes) for reusable cup return stations.
2. **Profitability Analysis**: Evaluate the financial viability of the reusable cup deposit system by analyzing fixed and variable costs and comparing it to single-use cups.
3. **Service Optimization**: Propose strategies to improve the efficiency and effectiveness of the reusable cup return service, including user engagement and awareness campaigns.

---

## 🔍 Methodology

### 1. Data Collection and Feature Selection

- **Data Sources**: We collected data from Seoul Open Data Plaza, Naver Maps, public datasets, and surveys conducted between July and August 2024.
- **Features Collected**:
  - Pedestrian traffic volume
  - Distance to nearest subway/bus station
  - Number of nearby cafes and restaurants
  - Sales volume and official land price
  - Number of public facilities and trash bins
- **Variable Selection**: ElasticNet and Lasso Regression were used to identify key factors influencing location selection, removing multicollinearity between variables.

### 2. MCLP Algorithm

- **Goal**: Maximize the coverage of cafes by placing reusable cup return stations at strategic locations while ensuring no two stations are within 300 meters of each other.
- **Implementation**: We used the **SCIP optimization solver** to solve this problem, selecting 1,179 optimal locations in Seoul.
  
### 3. Profitability Analysis

- **Variables**:
  - C_disposable: Cost per single-use cup
  - C_reusable: Cost per reusable cup
  - C_operation: Collection and washing costs
  - C_machine: Installation cost of return machines
  - r: Reusable cup return rate
- **Cost Calculation**: We calculated initial investment, variable costs, and fixed costs for the operation of the reusable cup system, comparing monthly profitability with different return rates.
  
---

## Key Results

1. **MCLP Results**: We identified 1,179 optimal cafe locations for the reusable cup return stations, with an average of 17.76 cafes covered per return station.
2. **Profitability**: At a 50% return rate, using reusable cups instead of single-use cups could generate an additional monthly profit of 777,800 KRW for a cluster of 31 cafes. Higher return rates would further increase profitability.
  
---

## Conclusion

This project demonstrates the environmental and economic benefits of implementing a reusable cup return system in Seoul. By selecting optimal return station locations and analyzing the financial impact, we have shown that this system can be both sustainable and profitable. Further work will focus on increasing consumer awareness and optimizing the system for other regions and facilities beyond cafes.

---

# ♻️ 서울시 다회용컵 반납기 입지 선정 및 서비스 고도화 방안

**2024 Data Analysis for Business (DAB) 제5회 경진대회, 고려대 경영대학**
*장려상 - 2024년 11월*

**Team Dolrido**  
*팀원: 김나연 (통계학), 김예은 (통계학), 배지원 (경제학), 정하연 (경영학), 최주희 (미디어학부)*  

## 🚀 개요

이 프로젝트는 **최대 커버리지 입지 문제(MCLP)** 알고리즘을 활용하여 서울시 내 다회용컵 반납기기의 최적 입지를 선정하고, 보증금 제도를 운영하는 다회용컵 서비스의 수익성을 분석하는 데 중점을 두고 있습니다. 플라스틱 컵 사용을 줄이고, 환경에 기여하며, 다회용컵 사용을 확산하는 것이 목표입니다.

---

## 💡 프로젝트 목표

1. **MCLP 알고리즘 적용**: 다회용컵 반납기를 최적 위치에 설치하여 최대한 많은 카페를 커버할 수 있는 전략을 도출합니다.
2. **수익성 분석**: 일회용컵과 비교하여 다회용컵 보증금 제도의 고정비 및 변동비를 분석하고, 경제적 타당성을 평가합니다.
3. **서비스 고도화**: 사용자 참여를 높이고, 서비스 운영을 효율적으로 개선하기 위한 방안을 제안합니다.

---

## 🔍 방법론

### 1. 데이터 수집 및 변수 선정

- **데이터 출처**: 서울 열린 데이터 광장, 네이버 지도, 공공 데이터 포털, 설문조사(2024년 7월~8월) 등에서 데이터를 수집하였습니다.
- **수집 변수**:
  - 유동 인구수
  - 지하철/버스 정류장까지의 거리
  - 주변 카페 및 음식점 개수
  - 매출 추정액 및 공시지가
  - 공공시설 및 가로 쓰레기통 수
- **변수 선택**: ElasticNet과 Lasso 회귀를 사용하여 다중공선성을 제거하고, 주요 변수를 도출하였습니다.

### 2. MCLP 알고리즘

- **목표**: 300m 이내의 중복을 피하면서 최대한 많은 카페를 커버할 수 있는 위치에 반납기를 설치하는 것입니다.
- **구현**: **SCIP 최적화 솔버**를 사용하여 서울시 내 1,179개의 최적 위치를 선정하였습니다.
  
### 3. 수익성 분석

- **주요 변수**:
  - C_disposable: 일회용컵 개당 비용
  - C_reusable: 다회용컵 개당 비용
  - C_operation: 수거 및 세척 비용
  - C_machine: 회수기 설치 비용
  - r: 다회용컵 회수율
- **비용 계산**: 초기 투자 비용, 변동비, 고정비를 계산하여 월별 수익을 분석하고, 회수율에 따른 수익성을 평가했습니다.
  
---

## 주요 결과

1. **MCLP 결과**: 서울시 내 1,179개의 최적 입지를 선정하였으며, 각 반납기는 평균 17.76개의 카페를 커버하는 것으로 나타났습니다.
2. **수익성**: 50%의 회수율에서 일회용컵 사용 대신 다회용컵을 사용할 경우, 클러스터 내 31개의 카페가 약 777,800원의 추가 수익을 얻을 수 있었습니다. 회수율이 높아질수록 수익은 더욱 증가합니다.
  
---

## 결론

본 프로젝트는 서울시에서 다회용컵 반납기 도입의 환경적 및 경제적 효과를 보여줍니다. 최적 입지 선정을 통해 다회용컵 서비스가 지속 가능하면서도 수익성을 가질 수 있음을 확인하였으며, 향후 다른 도시 및 시설에서도 적용할 수 있는 가능성을 제시합니다.
