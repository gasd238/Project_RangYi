# 디스코드 랑이 봇 #
이 봇은 학교 친구들과 디스코드 방에서 사용하기 위한 목적으로 처음 제작되었고 현재는 개인적으로 개발하는 용도로 제작되고 있습니다.

## Contact
문제 생기거나 궁금한점이 있을시 discord bluerain#5446 또는 gasd238@naver.com 으로 메일 주시면 빠르게 답해드리겠습니다.

## Requirements ##

이번에 따로 requirements.txt 로 정리 해두었습니다. pip install -r requirements.txt로 실행해 다운받아주세요.  
python ver = 3.10.6

## 랑이봇 사용법 ##

1. 위 requirement 에 있는 것들을 다운 받기
 - 파이썬 라이브러리들은 `pip install -r requirements.txt` 명령을 통해 설치 가능합니다.

2. 봇 토큰 설정
 - 먼저 디스코드 봇을 만들기 만드는 방법은 [여기](https://blog.naver.com/wpdus2694?Redirect=Log&logNo=221192640522) 
 - 만든 후 봇 토큰을 복사해 `Modules` 폴더에 `setting.py` 파일을 만들어주세요.
 - 파일에 `token=` 이라고 적고, 뒤에 당신의 봇 토큰을 적어주세요.
 - 그다음 `app.py`를 실행 해서 
 
 Logged in as
 
 (당신의 봇 이름)
 
 (봇 id)
 
  이렇게 출력됐을시 성공

 - 디스코드 봇을 만드는 방법에 나온 서버에 봇 추가하는 방법대로 원하는 서버에 봇을 추가하면 됨 (단 당신이 관리자 권한을 가지고 있는 서버만 )

## 참고 ##
`app.py` 실행을 중지 했을시 봇도 함께 꺼짐. 봇을 24시간 운영하고 싶으시다면 라즈베리 파이 같은 호스팅 방법을 찾으시면 됩니다.


## 기능 ##

**1. 유튜브 검색**

유튜브에서 영상을 검색해 총 10개의 결과를 출력

**2. 사진 검색**

구글에서 사진 검색해서 올림 (현재 성인인증으로만 볼 수 있는 사진들이 나오는 문제가 있음)

**3. 댓글 삭제**

말그대로 디코 대화를 삭제해줌

**4. 레벨 관련 기능**

우리가 디코로 대화 하면 그 양에 따라 레벨이 오르는 기능 레벨과 관련 기능은 [startergate](https://github.com/startergate)님의 도움으로 제작되었습니다. (setting.py 에 mongodb 주소를 넣어야합니다.)

**5. 야구 점수 출력**

야구 경기가 진행중일때만 사용 가능한 기능이며 야구 팀명을 입력시 (두산 베어스라면 두산만) 현재 점수와 이닝 양팀 투수를 출력합니다.(사이트에서 가져오는 것으로 실제보다 조금 느릴 수 있음)

**6. Yacht DICE 게임 기능**

트위치 등에서 흔히 야추 라고 불리던 yacht dice를 구현하였습니다. 혼자 또는 친구와 2인 플레이가 가능하며 버그 발견시 위 Contact 혹은 깃허브 페이지 issue로 올려주시면 됩니다.