# 디스코드 랑이 봇 #
이 봇은 개인적으로 만들어질 목적이었으나 외국~~노동~~문화 동아리 디스코드 서버에서 만들게 되면서 대규모 프로젝트로 바뀌어 버린 봇입니다.
## Requirements ##
이번에 따로 requirements.txt 로 정리 해두었습니다. pip install -r requirements.txt로 실행해 다운받아주세요.

## 랑이봇 사용법 ##

1. 위 requirement 에 있는 것들을 다운 받기
 - 파이썬 라이브러리들은 `pip install -r requirements.txt` 명령을 통해 설치 가능합니다.
 - 2번은 환경 변수 설정 해야 사용 가능 방법은 [여기](http://blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221165275268&parentCategoryNo=&categoryNo=112&viewDate=&isShowPopularPosts=false&from=postView)
 - 3번은 함께 올려 놓았음으로 설치된 위치만 알아두시면 됩니다.(search.py 파일에 있는 크롬드라이버 위치를 당신 컴퓨터 기준에 맞게 바꾸시면 됩니다.)
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

**2. 아침운동 기능**

명문 고등학교 GSM에서 실시하는 기숙사 아침운동이 다음날 할지 안할지를 알려줍니다.

**3. 노래 틀기**

디스코드 음성방에 노래를 틀어준다 (예약기능이 있어 편안)

**4. 유튜브 검색**

유튜브에서 영상을 검색해 총 10개의 결과를 출력

**5. 사진 검색**

구글에서 사진 검색해서 올림 (현재 성인인증으로만 볼 수 있는 사진들이 나오는 문제가 있음)

~~**6. 랑이 연애 시뮬레이터**~~ 취소됨

~~랑이 연애 시뮬레이터 제작 중 (스토리 및 약간의 기능 제외 완성)~~

**7. 발표 순서 정하기**

코드에 평소 자주 순서 정하는 사람들은 코드에 넣고 가끔씩 정하는 사람들은 따로 `!발표 [누구] [누구]` 이런식으로 입력하면 됨

**8. 댓글 삭제**

말그대로 디코 대화를 삭제해줌

~~**9. 고소 관련 기능**~~  약간의 수정을 거칠 예정입니다.

~~디코 대화중 말싸움이 생겼을시 관리자와 싸움이 발생한 2사람이 관리자와 2사람 제외 

~~볼 수 없는 방에서 조용히 해결하고 나오는 기능

**10. 학교 일정 출력 기능**

광주소프트웨어마이스터고등학교에 그달 일정을 가지고와 깔끔(?)하게 출력해주는 기능

**11. 레벨 관련 기능**

우리가 디코로 대화 하면 그 양에 따라 레벨이 오르는 기능 레벨과 관련 기능은 [startergate](https://github.com/startergate)님의 도움으로 제작되었습니다.
