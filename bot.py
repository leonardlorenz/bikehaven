import discord

ESCAPE = '!setroles'
ALL_ROLES = {
        'wethepeople' : '589581183567003648',
        'eclat'       : '589581291465211927',
        'odyssey'     : '589581555161366534',
        'sunday'      : '589581632814448681',
        'fitbikeco'   : '589581665832009729',
        'eastern'     : '589581794920103960',
        'stranger'    : '589581857813823491',
        'bsd'         : '589581908690731008',
        's&m'         : '589581183567003648',
        'sandm'       : '589581183567003648',
        'cult'        : '589582163431915520',
        'colony'      : '589582423461724359',
        'fiend'       : '589582518366240789',
        'kink'        : '589582607621160981',
        'subrosa'     : '589582636356337692',
        'tallorder'   : '589581183567003648',
        'volume'      : '589582833945935884',
        'total'       : '589582908767993886',
        'hyper'       : '589583999333040161',
        'federal'     : '589892467005063169',
        'primo'       : '589892521652518948',
        'haro'        : '589892903699087386',
        'animal'      : '589893431044603945',
        'academy'     : '589895576376574081',
        'shadow'      : '589895638058139669',
        'merrit'      : '589896707362390042',
        'profile'     : '589935838830395393',
        'madera'      : '589937553180721155',
        'gsport'      : '589937619723354113',
        }

class bot(discord.Client):
    @client.event
    async def on_ready()
        print('Logged on as {}!'.format(self.user))

        # set up roles


    @client.event
    async def on_message(self, message)
        content = message.content

        if message.author == self.user:
            return

        if content.startswith(ESCAPE):
            roles = content.split(' ')[1:$]
            if roles[1] == 'showroles':
                # TODO print all the roles
                pass
            for role in roles:
                if role.lower in ALL_ROLES:
                    # get guild of message and from there the role that got requested
                    role = message.guild.get_role(ALL_ROLES[role.lower])
                    message.author.add_roles(role, reason='Requested via bikehaven bot.')
                else:
                    message.channel.send('the role ' + role + ' does not exist. Use \`' + ESCAPE + ' showroles\` to display all the available roles')
            pass

    token = read_token()


def read_token():
    token_file = open('token.txt')
    token = token_file.readlines()[0].strip("\n")
    token_file.close()
    return token

if __name__ == '__main__':
    main()
