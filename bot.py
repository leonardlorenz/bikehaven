import discord

escape = '!setroles'
roles = []

class bot(discord.Client):
    @client.event
    async def on_ready()
        print('Logged on as {}!'.format(self.user))
        roles = get_roles()

    @client.event
    async def on_message(self, message)
        if message.author == self.user:
            return

        if message.content.startswith('escape'):
            pass

    token = read_token()


def read_token():
    token_file = open('token.txt')
    token = token_file.readlines()[0].strip("\n")
    token_file.close()
    return token

if __name__ == '__main__':
    main()
