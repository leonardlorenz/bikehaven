#!/home/bikehaven/bikehaven/venv/bin/python3
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import get
from roles import Roles

PREFIX = '?'
bot = commands.Bot(command_prefix=PREFIX)

@bot.command()
async def ping(ctx):
    '''
    : Bot answers with pong
    '''
    await ctx.send('pong')

@bot.command(pass_context=True)
async def setroles(ctx):
    '''
    : Set roles via ?setroles <role1> <role2>
    '''
    roles_to_add = ctx.message.content.split(' ')[1:]
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
                        await this_member.add_roles(this_role)
                        await ctx.send('Added **' + role_name + '** to ' + str(this_member) + '!')
                        role_set = True
                    except Exception as e:
                        print(e)
        if not role_set:
            await ctx.send(
                'The role **' + str(current_role) + '** does *not* exist. Use \n> **' + PREFIX + 'showroles**\nto display all the available roles.')

@bot.command(pass_context=True)
async def removeroles(ctx):
    '''
    : Remove roles that you don't want anymore
    '''
    roles_to_remove = ctx.message.content.split(' ')[1:]
    exception_thrown = False

    for current_role in roles_to_remove:
        role_removed = False
        for role_name, role_id in Roles.ALL_ROLES.items():
            if current_role.lower() == role_name.lower():
                this_member = ctx.message.author
                this_guild = this_member.guild
                this_role = get(this_guild.roles, id=int(role_id))
                if this_role is not None:
                        member_had_group = False
                        for this_member_role in this_member.roles:
                            if this_role == this_member_role:
                                try:
                                    await this_member.remove_roles(this_role)
                                    await ctx.send('Removed **' + str(role_name) + '** from ' + str(this_member) + '!')
                                    role_removed = True
                                except Exception as e:
                                    exception_thrown = True
                                    await ctx.send(str(e))
                        if not member_had_group and not exception_thrown and not role_removed:
                            exception_thrown = True
                            await ctx.send(
                                'The user **' + str(this_member) + '** does *not* have the role **' + str(this_role) + '**. Use \n> **' + PREFIX + 'showroles**\nto display all the available roles.')
                            # break loop to not send 'role does not exist' exception below
                            break
        if not role_removed and not exception_thrown and not role_removed:
            await ctx.send(
                'The role **' + str(current_role) + '** does *not* exist. Use \n> **' + PREFIX + 'showroles**\nto display all the available roles.')



@bot.command(pass_context=True)
async def showroles(ctx):
    '''
    : Shows all available BMX roles
    ''' msg = ""
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

@bot.event
async def on_command_error(ctx, error):
    # if no matching command was found print the error message to the chat
    if isinstance(error, CommandNotFound):
        await ctx.send(
            'The command **' + ctx.message.content.split(' ')[0] + '** does *not* exist. Use \n> **' + PREFIX + 'help**\nto display all the available commands.')
        return

def read_token():
    token_file = open('token.txt')
    token = token_file.readlines()[0].strip("\n")
    token_file.close()
    return token

TOKEN = read_token()
bot.run(TOKEN)
