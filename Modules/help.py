# -*-coding: UTF-8-*-
import nextcord


class Help:
    def create_help_embed(self):
        embed = nextcord.Embed(
            title="나와 노는 법이니라!!",
            description="나를 이 서버에 초대해 주어서 정말 고맙느니라 너희들을 위해 많은 걸 준비했으니 많이많이 사용해 주거라~~",
            color=0xF7CAC9,
        )
        embed.add_field(
            name="!초대", value="디코방에 나를 초대하는 방법 안내 이니라!", inline=False
        )
        embed.add_field(
            name="!삭제 [갯수]",
            value="메세지를 삭제하는 기능이니라~ 단 99개 이하만 삭제할 수 있느니라...",
            inline=False,
        )
        embed.add_field(
            name="!검색 [제목]", value="유튜브에서 영상을 검색해 링크를 보내주는 기능이니라~", inline=False
        )
        embed.add_field(
            name="!사진 [찾을 것]", value="찾는것에 대한 사진을 보내주는 기능이니라~", inline=False
        )
        # embed.add_field(name='!고소 [할 사람 언급]', value='상대방과 합의방에서 1대1로 대화하게 해주는 기능이니라!', inline=False)
        # embed.add_field(name='!취하 [할 사람 언급]', value='고소를 잘못했거나 끝났을 때 쓰는 기능이니라!', inline=False)
        embed.add_field(
            name="!레벨 [@유저]",
            value="자신의 레벨과 남은 경험치 또는 다른 사람의 레벨을 표시하는 기능이니라",
            inline=False,
        )
        embed.add_field(name="!랭킹", value="레벨 1위부터 10위까지 출력하는 기능이니라~", inline=False)
        embed.add_field(
            name="!야구 [팀명]",
            value="야구 경기중에만 사용 가능한 기능으로 야구 경기 점수를 보여줍니다. ※(KIA 타이거즈라면 KIA만 입력해 주세요, 팀명이 영어면(kia, sk 등)영어로 입력해주세요)",
            inline=False,
        )
        embed.set_author(
            name="랑이",
            icon_url="https://raw.githubusercontent.com/gasd238/Project_RangYi/master/rang%20pic.jpg",
        )
        return embed
