import discord
import requests
import json
from discord.ext import tasks, commands

count = 0

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = "YOUR_BOT_TOKEN"

headers = {
    'Referer': 'https://www.oref.org.il//12481-he/Pakar.aspx',
    'X-Requested-With': 'XMLHttpRequest',
}

#------------------Discord functions-----------------------
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="rockets from Gaza")
    await bot.change_presence(activity=activity)
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    global channel
    channel = ctx.message.channel
    check_alerts.start()
    await ctx.send(f"Alert monitoring started in #{channel.name}")


@bot.command()
async def stop(ctx):
    check_alerts.stop()
    await ctx.send("Alert monitoring stopped.")
#------------------Discord functions-----------------------

sent_alert_ids = set()


@tasks.loop(seconds=3)  
async def check_alerts():
    global count
    try:
        #url = "https://vocal-churros-945d25.netlify.app/data.json" This is how I tested the alerts on my own, lol.
        url = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
        response = requests.get(url,headers=headers)
        response_content = response.content.decode('utf-8-sig')
        print(f"Response:{response_content}")
        print(response.status_code)
        
        requiretext = "1"
        try:
            if requiretext in response_content:
                data = json.loads(response_content)
                alert_id = data["id"]

                if alert_id not in sent_alert_ids:
                    sent_alert_ids.add(alert_id)
                    alert_location = data["data"]
                    alert_time = data["desc"]
                    embed_message = {
                        "type": "rich",
                        "title": f"ירי טילים ורקטות ב{alert_location}",
                        "description": f"***צבע אדום:  {alert_location}***",
                        "color": 0xff1313,
                        "fields": [
                            {
                                "name": f"{alert_time}",
                                "value": "\u200B"
                            }
                        ],
                        "thumbnail": {
                            "url": "https://emoji.discadia.com/emojis/8a3aac2a-d23d-4aa9-a7a9-cc60ce82fca3.GIF",
                            "height": 0,
                            "width": 0
                        },
                        "footer": {
                            "text": "Made by no1se",
                            "icon_url": "https://emoji.discadia.com/emojis/8a3aac2a-d23d-4aa9-a7a9-cc60ce82fca3.GIF"
                        }
                    }
                    
                    
                    await channel.send(embed=discord.Embed.from_dict(embed_message))
        except Exception as e:
            print("Something went wrong but I'm still sending requests...")
            print(f"Error:  {e}")           
        else:
            count += 1
            print(f"No alerts at the moment. number of tries:{count}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")



bot.run(TOKEN)


#Made by no1se
