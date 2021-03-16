#-*-coding: UTF-8-*-
import discord

class Help:
    def create_help_embed(self):
        embed = discord.Embed(title="나와 노는 법이니라!!",description="나를 이 서버에 초대해 주어서 정말 고맙느니라 너희들을 위해 많은 걸 준비했으니 많이많이 사용해 주거라~~", color=0xf7cac9)
        # embed.add_field(name = '!급식', value = '오전 8시, 오후 1시, 오후 7시를 기점으로 아침, 점심, 저녁이 바뀌어서 출력되느니라~(금요일 오후 1시부터 일요일 7시까지 급식이 없다고 표시되느니라~~)',inline = False)
        embed.add_field(name='!분양', value='디코방에 나를 데려갈 수 있는 링크를 보내줄 것이니라~', inline=False)
        # embed.add_field(name='!아침운동', value='다음날 아침에 미세먼지 상황과 날씨를 불러와 할지 안할지 알려주는 기능이니라~', inline=False)
        embed.add_field(name='!삭제 [갯수]', value='메세지를 삭제하는 기능이니라~ 단 99개 이하만 삭제할 수 있느니라...', inline=False)
        embed.add_field(name='!검색 [제목]', value='유튜브에서 영상을 검색해 링크를 보내주는 기능이니라~', inline=False)
        embed.add_field(name='!사진 [찾을 것]', value='찾는것에 대한 사진을 보내주는 기능이니라~', inline=False)
        # embed.add_field(name='!고소 [할 사람 언급]', value='상대방과 합의방에서 1대1로 대화하게 해주는 기능이니라!', inline=False)
        # embed.add_field(name='!취하 [할 사람 언급]', value='고소를 잘못했거나 끝났을 때 쓰는 기능이니라!', inline=False)
        # embed.add_field(name='!일정', value='그 달에 있는 학교 일정을 불러오는 기능이니라!', inline=False)
        # embed.add_field(name='!랭킹', value='레벨 1위부터 10위까지 출력하는 기능이니라~', inline=False)
        embed.add_field(name='!야구 [팀명]', value='야구 경기중에만 사용 가능한 기능으로 야구 경기 점수를 보여줍니다. ※(KIA 타이거즈라면 KIA만 입력해 주세요, 팀명이 영어면(kia, sk 등)영어로 입력해주세요)', inline=False)
        embed.set_author(name="랑이", icon_url="https://raw.githubusercontent.com/gasd238/rangyibot-host/master/rang%20pic.jpg?token=AJZS3UHJMLBIINDC54WKTVDAKC22M")
        return embed
