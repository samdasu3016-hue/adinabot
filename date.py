import discord
from discord import app_commands
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class attendanceBot(discord.Client):
     def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.data_file = "attendance_data.json"
        self.attendance = self.load_data()

     def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

     def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.attendance, f, ensure_ascii=False, indent=4)

     async def on_ready(self):
        await self.tree.sync()  # 슬래시 명령어를 디스코드 서버와 동기화
        print(f"실행 완료: {self.user}")

bot = attendanceBot()

@bot.tree.command(name="출석", description="오늘의 출석을 기록한다요!")
async def 출석(interaction: discord.Interaction):
    user = interaction.user
    today = str(date.today())

    if str(user.id) not in bot.attendance:
        bot.attendance[str(user.id)] = {"last_date": today, "count": 1, "username": str(user)}
        bot.save_data()
        await interaction.response.send_message(f"{user.mention}, 첫 출석체크 했다요! (누적 1일차)")
        return
    
    user_data = bot.attendance[str(user.id)]
    last_date = user_data["last_date"]

    if user_data["last_date"] == today:
        await interaction.response.send_message(f"{user.mention}, 이미 오늘 출석했다요! (누적 {user_data['count']}일차)", ephemeral=True)
        return
    
    yesterday = str(date.today() - timedelta(days=1))
    if last_date == yesterday:
        user_data["streak"] += 1
    else:
        user_data["streak"] = 1

    user_data["last_date"] = today
    user_data["count"] += 1

    bot.save_data()
    await interaction.response.send_message(f"{user.mention}, 오늘도 안녕하다요!\n (누적 {user_data['count']}일차/연속 {user_data['streak']}일차)")


bot.run(TOKEN)# 실제 봇 토큰임 이거유출되면좃됨
print("TOKEN:", TOKEN)
