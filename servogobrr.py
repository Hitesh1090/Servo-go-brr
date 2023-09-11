import discord
from discord.ext import commands
import random
import serial
import time

intents = discord.Intents.all()
intents.message_content = True  
intents.members=True
serial_port = 'PORT_ID'
spin_gifs=['SPINNING_GIF_URLs']

nope_gifs=['NAAH_GIF_URLs']

welcome_gif=['WELCOME_GIF_URLs']
ser = serial.Serial(serial_port, 9600, timeout=1)

bot = commands.Bot(command_prefix='!', intents=intents)

min_angle = 0
max_angle = 180

def send_command(command):
    ser.write(command.encode())

def Rotate():
    for angle in range(min_angle, max_angle + 1):
        send_command(f'S{angle}\n')
        time.sleep(0.005) 

    for angle in range(max_angle, min_angle - 1, -1):
        send_command(f'S{angle}\n')
        time.sleep(0.005) 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel=member.guild.system_channel
    instructions = "Here's how to use the bot:\n" \
                   "- Use !rotate (angle) to rotate the servo to the specified angle \n" \
                   "[ Pick an integer from 0 to 180 ] \n" \
                   "- @Mention the server op and request for video footage if you want to see it in action \n" \
                   "- Try not to be cocky and spam the command, cuz theres a 2 second cooldown \n" \
                   "- Use !udhavi for getting these instructions again in the future" 
                   
    embed=discord.Embed(title='Welcome to this useless fuckin server',description=instructions,color=discord.Color.blue())
    embed.set_image(url=welcome_gif[0])            
    
    await channel.send(embed=embed)

@bot.command(name="udhavi", description="Instructions for the ServoBrr bot")
async def udhavi(ctx):
    instructions = "Welcome to the server! Here's how to use the bot:\n" \
                   "- Use !rotate (angle) to rotate the servo to the specified angle \n" \
                   "[ Pick an integer from 0 to 180 ] \n" \
                   "- @Mention the server op and request for video footage if you want to see it in action \n" \
                   "- Try not to be cocky and spam the command, cuz theres a 2 second cooldown"
                   
    embed=discord.Embed(title="Instructions",description=instructions,color=discord.Color.purple())
    
    
    await ctx.send(embed=embed)

@bot.command(name="rotate", description="to go brr")
@commands.cooldown(1, 2, commands.BucketType.user)  
async def rotate(ctx,angle):
        if 0 <= angle <= 180:
            Rotate(angle)
            embed = discord.Embed(title="Servo Indeed Went Brrrr",
                                description=f"Rotated the servo motor to {angle} degrees",
                                color=discord.Color.green())
            embed.set_image(url=spin_gifs[random.randint(0, 8)])
        else:
            embed = discord.Embed(title="Nah Fam",
                                description="Angle should be between 0 and 180 degrees.",
                                color=discord.Color.red())
            embed.set_image(url=nope_gifs[random.randint(0, 7)])
        await ctx.send(embed=embed)

@rotate.error
async def rotate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        timeout_embed = discord.Embed(
            title="Cooldown",
            description=f"This command is on a 2 sec cooldown. Try again in {round(error.retry_after, 2)} seconds.",
            color=discord.Color.red()
        )
        timeout_embed.set_image(url=nope_gifs[random.randint(0,7)])
        await ctx.send(embed=timeout_embed)

bot.run('YOUR_BOT_ID_HERE')
