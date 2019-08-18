import discord
from discord.ext import commands
from discord.utils import get
from roles import Roles

PREFIX = '?'
bot = commands.Bot(command_prefix=PREFIX)

@bot.command()
async def ping(ctx):
    '''
    Bot answers with pong
    '''
    await ctx.send('pong')

@bot.command(pass_context=True)
async def setroles(ctx):
    '''
    Set roles via {}setroles <role1> <role2>
    '''.format(PREFIX)
    roles_to_add = ctx.message.content.split(' ')[1:]
    print(roles_to_add)
    # TODO check if user has role already
    for current_role in roles_to_add:
        role_set = False
        for role_name, role_id in Roles.ALL_ROLES.items():
            if current_role.lower() == role_name.lower():
                this_member = ctx.message.author
                this_guild = this_member.guild
                this_role = get(this_guild.roles, id=int(role_id))
                print("trying to set role... ")
                print("\t" + str(this_guild))
                print("\t" + str(this_member))
                print("\t" + str(this_role))
                if this_role is not None:
                    try:
                        await this_member.add_roles(this_member, this_role)
                        role_set = True
                    except Exception as e:
                        print(e)
        if not role_set:
            await ctx.send(
                'The role **' + current_role + '** does *not* exist. Use \n> **' + PREFIX + 'showroles**\nto display all the available roles')

@bot.command(pass_context=True)
async def showroles(ctx):
    '''
    Shows all available BMX roles
    '''
    msg = ""
    for role in Roles.ALL_ROLES:
        msg += "> " + role + "\n"
    await ctx.send(msg)

@bot.event
async def on_ready():
    print("Bot running!")

@bot.event
async def on_message(message):
    print(message.content)
    await bot.process_commands(message)

def read_token():
    token_file = open('token.txt')
    token = token_file.readlines()[0].strip("\n")
    token_file.close()
    return token

TOKEN = read_token()
bot.run(TOKEN)
