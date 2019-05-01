#-*-coding: UTF-8-*-
import discord


class Help:
    def create_help_embed():
        embed = discord.Embed(title="이 봇은 매--우 공적인 목적으로 만들어졌느니라~",description="이 봇은 제작자가 나를 위해 만들어준 봇으로 GSM에 여러 편의 기능을 지원하고 있느니라~ 많이 많이 이용해 주거라~", color=0xf7cac9)
        embed.add_field(name = '!급식', value = '오전 8시, 오후 1시, 오후 7시를 기점으로 아침, 점심, 저녁이 바뀌어서 출력되느니라~(금요일 오후 1시부터 일요일 7시까지 급식이 없다고 표시되느니라~~)',inline = False)
        embed.add_field(name='!분양', value='너의 디코방에 나를 데려갈 수 있는 링크를 보내줄 것이니라~', inline=False)
        embed.add_field(name='!아침운동', value='다음날 아침에 미세먼지 상황과 날씨를 불러와 할지 안할지 알려주는 기능이니라~', inline=False)
        embed.add_field(name='!재생 [링크]', value='노래를 재생하니라~.', inline=False)
        embed.add_field(name='!종료', value='노래 재생을 멈추고 음성방에서 나갈 것이니라~', inline=False)
        embed.add_field(name='!예약 [링크]', value='처음 재생될 노래 다음에 나올 노래들을 예약하는 기능이니라~', inline=False)
        embed.add_field(name='!큐 보기/삭제', value='보기는 재생목록을 모두 보여주고 삭제는 모든 예약곡을 삭제하느니라~', inline=False)
        embed.add_field(name='!삭제 [갯수]', value='메세지를 삭제하는 기능이니라~ 단 99개 이하만 삭제할 수 있느니라...', inline=False)
        embed.add_field(name='!발표', value='발표 순서를 랜덤으로 결정해주는 기능이니라~ ', inline=False)
        embed.add_field(name='!검색 [제목]', value='유튜브에서 영상을 검색해 링크를 보내주는 기능이니라~', inline=False)
        embed.add_field(name='!사진 [찾을 것]', value='찾는것에 대한 사진을 보내주는 기능이니라~', inline=False)
        embed.add_field(name='!고소 [할 사람 언급]', value='상대방과 합의방에서 1대1로 대화하게 해주는 기능이니라!', inline=False)
        embed.add_field(name='!취하 [할 사람 언급]', value='고소를 잘못했거나 끝났을 때 쓰는 기능이니라!', inline=False)
        embed.add_field(name='!일정', value='그 달에 있는 학교 일정을 불러오는 기능이니라!', inline=False)
        embed.add_field(name='!랭킹', value='레벨 1위부터 10위까지 출력하는 기능이니라~', inline=False)
        embed.set_author(name="랑이", icon_url="https://postfiles.pstatic.net/MjAxOTA0MDFfMjIg/MDAxNTU0MDc1MzgxODEz.GprXtmnHfiMPpay2riQUAJQZTtLghpxjXyxFUV2hj0og.oair81q3mrLQqZcqegADwVMNOyYCoNTd429vxqgXlwkg.JPEG.gasd238/help.jpg?type=w580")
        embed.set_image(url="https://postfiles.pstatic.net/MjAxOTA0MDFfMjIg/MDAxNTU0MDc1MzgxODEz.GprXtmnHfiMPpay2riQUAJQZTtLghpxjXyxFUV2hj0og.oair81q3mrLQqZcqegADwVMNOyYCoNTd429vxqgXlwkg.JPEG.gasd238/help.jpg?type=w580")
        return embed
