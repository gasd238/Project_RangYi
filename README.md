# 디스코드 랑이 봇 #
이 봇은 개인적으로 만들어질 목적이었으나 외국~~노동~~문화 동아리 디스코드 서버에서 만들게 되면서 대규모 프로젝트로 바뀌어 버린 봇입니다.

## Contact
문제 생기거나 궁금한점이 있을시 discord bluerain#5446 또는 gasd238@naver.com 으로 메일 주시면 빠르게 답해드리겠습니다.

## Requirements ##

이번에 따로 requirements.txt 로 정리 해두었습니다. pip install -r requirements.txt로 실행해 다운받아주세요.

## 랑이봇 사용법 ##

1. 위 requirement 에 있는 것들을 다운 받기
 - 파이썬 라이브러리들은 `pip install -r requirements.txt` 명령을 통해 설치 가능합니다. 
 - 1번은 3.6 이하 버전을 사용을 권장 합니다.(3.7이상 버전에서 사용이 안되는것으로 확인됨)

2. 봇 토큰 설정
 - 먼저 디스코드 봇을 만들기 만드는 방법은 [여기](https://blog.naver.com/wpdus2694?Redirect=Log&logNo=221192640522) 
 - 만든 후 봇 토큰을 복사해 `Modules` 폴더에 `setting.py` 파일을 만들어주세요.
 - 파일에 `token=` 이라고 적고, 뒤에 당신의 봇 토큰을 적어주세요.
 - 그다음 `Project_RangYi_Bot.py`를 실행 해서 
 
 Logged in as
 
 (당신의 봇 이름)
 
 (봇 id)
 
  이렇게 출력됐을시 성공

 - 디스코드 봇을 만드는 방법에 나온 서버에 봇 추가하는 방법대로 원하는 서버에 봇을 추가하면 됨 (단 당신이 관리자 권한을 가지고 있는 서버만 )

## 참고 ##
`Project_RangYi_Bot.py` 실행을 중지 했을시 봇도 함께 꺼짐. 봇을 24시간 운영하고 싶으시다면 라즈베리 파이 같은 호스팅 방법을 찾으시면 됩니다.


## 기능 ##

**1. 급식 크롤링**

명문 고등학교 광주 소프트웨어 마이스터고(통칭: GSM)의 급식을 불러옵니다

~~**2. 아침운동 기능**~~ 날씨 보는 기능으로 변경 예정

~~명문 고등학교 GSM에서 실시하는 기숙사 아침운동이 다음날 할지 안할지를 알려줍니다. (다음날 날씨 및 미세먼지 정보를 크롤링으로 불러와 확인)~~  
아침운동이 날씨가 어떻게 되는 실시되었고 2020년은 코로나로 인해 시행되지 않았습니다. 이로 인해 날씨 확인 기능으로 변경 예정입니다.

**3. 유튜브 검색**

유튜브에서 영상을 검색해 총 10개의 결과를 출력

**4. 사진 검색**

네이버 api로 변경 api사용법은 나중에 추가 예정  

**5. 댓글 삭제**

말그대로 디코 대화를 삭제해줌

~~**6. 레벨 관련 기능**~~ 현재 약간의 수정을 거쳐 다시 켤 예정입니다.

~~디코로 대화시 특정 조건에 따라 레벨이 오르는 기능으로 관련 기능은 [startergate](https://github.com/startergate)님의 도움으로 제작되었습니다.~~

**7. 야구 점수 출력**

야구 경기가 진행중일때만 사용 가능한 기능이며 야구 팀명을 입력시 (두산 베어스라면 두산만) 현재 점수와 이닝 양팀 투수를 출력합니다.(사이트에서 가져오는 것으로 실제보다 조금 느릴 수 있음)

**8. 야추 다이스 게임**

51 Worldwide Games에 수록된 Yacht dice 게임을 구현해 보았습니다. 버그가 조금씩 존재할 수 있으며 버그 발견시 연락 주시면 좋겠습니다.
