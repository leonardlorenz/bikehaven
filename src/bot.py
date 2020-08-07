#/usr/bin/env python

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import get

with open('token.txt') as f:
    TOKEN = f.readlines()[0].strip("\n")

ALL_ROLES = {}

def reload_roles():
    with open('roles.txt') as f:
        ALL_ROLES.clear()
        lines = f.readlines()
        for l in lines:
            split = l.replace(" ", "").replace("\t", "").split(":")
            ALL_ROLES[split[0]] = split[1]

PREFIX = 'pls '

bot = commands.Bot(PREFIX)

@bot.command()
async def ping(ctx):
    '''
    : Bot answers with pong
    '''
    await ctx.send('pong')

@bot.command(pass_context=True)
async def set(ctx):
    '''
    : Set roles via "pls set role1 role2 roleN ..."
    '''
    reload_roles()

    roles_to_add = ctx.message.content.split(' ')[2:]

    for current_role in roles_to_add:
        role_set = False
        for role_name, role_id in ALL_ROLES.items():
            if current_role.lower() == role_name.lower():
                this_member = ctx.message.author
                this_guild = this_member.guild
                this_role = get(this_guild.roles, id=int(role_id))
                print("trying to set role... ")
                print("\t" + str(this_guild))
                print("\t" + str(this_member))
                print("\t" + str(this_role))
                if this_role:
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
async def remove(ctx):
    '''
    : Remove roles that you don't want anymore
    '''
    reload_roles()

    roles_to_remove = ctx.message.content.split(' ')[2:]
    exception_thrown = False

    for current_role in roles_to_remove:
        role_removed = False
        for role_name, role_id in ALL_ROLES.items():
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
async def show(ctx):
    '''
    : Shows all available BMX roles
    '''
    reload_roles()

    msg = ""
    for role in ALL_ROLES:
        msg += "> " + role + "\n"
    await ctx.send(msg)

@bot.event
async def on_ready():
    print("Bot running!")
    reload_roles()
    print("Roles loaded!")

@bot.event
async def on_message(message):
    print(message.content)
    if "tenor.com" in message.content:
        await message.channel.send("You may not send tenor GIFs. Sorry.")
        await message.delete()
    if message.channel.name == "botspam":
        await bot.process_commands(message)
    else:
        if message.content.startswith(PREFIX):
            await message.channel.send("I only work in #botspam.")

@bot.event
async def on_command_error(ctx, error):
    # if no matching command was found print the error message to the chat
    if isinstance(error, CommandNotFound):
        await ctx.send(
            'The command **' + ctx.message.content.split(' ')[0] + '** does *not* exist. Use \n> **' + PREFIX + 'help**\nto display all the available commands.')
        return

bot.run(TOKEN)
