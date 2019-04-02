# 디스코드 랑이 봇 #
이 봇은 개인적으로 만들어질 목적이었으나 외국~~노동~~문화 동아리 디스코드 서버에서 만들게 되면서 대규모 프로젝트로 바뀌어 버린 봇입니다.
## Requirements ##

1.**Python 3.6**

2.**discord.py**

3.**beautifulsoup4.py** 

4.**youtube_dl.py**

5.**ffmpeg** 

6.**chromedriver**

7.**lxml**

## 랑이봇 사용법 ##

1. 위 requirement 에 있는 것들을 다운 받기
 - 2, 3, 4, 7번 은 pip 를 통해 다운 가능
 - 5번은 환경 변수 설정 해야 사용 가능 방법은 [여기](http://blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221165275268&parentCategoryNo=&categoryNo=112&viewDate=&isShowPopularPosts=false&from=postView)
 - 6번은 함께 올려 놓았음으로 설치된 위치만 알아두시면 됩니다.(search.py 파일에 있는 크롬드라이버 위치를 당신 컴퓨터 기준에 맞게 바꾸시면 됩니다.)
 - 1번은 3.6 이하 버전을 사용을 권장 합니다.(3.7이상 버전 discord.py 사용 )

2. 봇 토큰 설정
 - 먼저 디스코드 봇을 만들기 만드는 방법은 [여기](https://blog.naver.com/wpdus2694?Redirect=Log&logNo=221192640522) 
 - 만든 후 봇 토큰을 복사해 Project_RangYi_Bot.py 파일 맨 아래 Bot_Token 부분을 당신의 봇 토큰으로 변경
 - 그다음 Project_RangYi_Bot.py를 실행 해서 
 
 Logged in as
 
 (당신의 봇 이름)
 
 (봇 id)
 
  이렇게 출력됬을시 성공

 - 디스코드 봇을 만드는 방법에 나온 서버에 봇 추가하는 방법대로 원하는 서버에 봇을 추가하면 됨(단 당신이 관리자 권한을 가지고 있는 서버만 )

## 참고 ##
Project_RangYi_Bot.py 실행을 중지 했을시 봇도 함께 꺼짐 봇을 24시간 운영하고 싶으시다면 라즈베리 파이 같은 호스팅 방법을 찾으시면 됩니다.
