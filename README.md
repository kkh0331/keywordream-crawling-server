# Keywordream Crawling Server
>Keywordream 프로젝트에서 Flask을 이용한 Crawling Server  
>`pythoon version` : 3.10.0

## 🔗 Link
리팩토링 전 링크
>https://github.com/Keywordream-PDA/Data

## 📝 크롤링 서버 구축한 이유
- 프로젝트 초기에는 실시간 크롤링을 Main Server에 붙일려고 했었음  
- But, 실시간 크롤링을 하는 도중에 에러가 발생할 경우 Main Server가 동작하지 않을 가능성이 있음  
- So 크롤링 서버를 따로 분리함  
- 크롤링, 키워드 추출, 뉴스 감정분석을 용이하게 하기 위해서 python을 이용한 Flask Server을 구축했음

## 🙋‍♂️ 담당한 기능
- Flask Server 구축
- 뉴스 크롤링 및 뉴스 감정분석
- 전체 코드 리팩토링

## 🗂️ Schema
### 리팩토링 전
<img src="https://github.com/user-attachments/assets/2b32f526-97da-4d0f-86ae-3f39d65c395f" width="600" height="auto">

### 리팩토링 후
<img src="https://github.com/user-attachments/assets/a1955503-06bc-44a9-b3d5-ee3c26b60dfd" width="600" height="auto">

## 😡 Trouble Issues
### 크롤링 최소화
>[Keywordream 프로젝트 후기](https://velog.io/@rlgus9301/Keywordream-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0) - 2. 뉴스 크롤링
- 원래는 사용자가 요청할 때마다, 크롤링을 진행하려고 했었음
- But, 중복 크롤링 가능성도 있고 크롤링을 하는 네이버에서 막을 가능성이 존재
- So, 크롤링을 최소화하기 위해 DB에 저장함으로써 중복 크롤링을 막음
- 대략 뉴스 크롤링 및 키워드 추출 시간을 평균 1/3 줄임
### 리팩토링
> [Keywordream 리팩토링 계획](https://velog.io/@rlgus9301/Keywordream-%EB%A6%AC%ED%8C%A9%ED%86%A0%EB%A7%81-%EA%B3%84%ED%9A%8D)
- 프로젝트 당시에 db 설계, api 설계 등 부족하여 리팩토링을 할 필요성을 느낌
- 메인 서버를 리팩토링하면서 크롤링 서버도 수정된 db에 맞춰서 리팩토링 진행
- [리팩토링 전] 크롤링을 제외한 거의 모든 코드가 app.py에 구현
- [리팩토링 후] mvc 패턴에 기반하여 코드들을 관련된 것들끼리 묶어서 구현

## 🗂️ Folder Structure 
### 리팩토링 전
```
├── README.md
├── app.py
├── crawling
│   ├── api.py
│   ├── bs4.py
│   └── crawling.py
├── db
│   ├── check_insert_stock.py
│   ├── check_news_id.py
│   ├── connect.py
│   ├── get_title_content.py
│   ├── insert_isGood.py
│   ├── insert_keywords.py
│   ├── insert_news.py
│   └── insert_news_stock.py
├── mecab
│   ├── Mecab-ko-for-Google-Colab
│   ├── mecab-0.996-ko-0.9.2.tar.gz
│   └── mecab-ko-dic-2.1.1-20180720.tar.gz
└── requirements.txt
```
### 리팩토링 후
```
├── README.md
├── app.py
├── client
│   └── naver_api.py
├── crawling
│   ├── repository.py
│   └── service.py
├── database
│   └── connect.py
├── keywords
│   ├── repository.py
│   └── service.py
├── mecab
│   ├── Mecab-ko-for-Google-Colab
│   ├── mecab-0.996-ko-0.9.2.tar.gz
│   └── mecab-ko-dic-2.1.1-20180720.tar.gz
├── news
│   ├── controller.py
│   ├── repository.py
│   └── service.py
├── requirements.txt
├── stocks
│   ├── controller.py
│   ├── repository.py
│   └── service.py
└── utils
    ├── api_result.py
    └── json_app.py
```
