import discord
from discord.ext import commands
import aiohttp

class stats_checker(commands.Cog):
    def __init__(self, bot):
        self.bot=bot  

    @commands.command()
    async def stats(self, ctx, wallet):

        embed = discord.Embed(title='<a:XVo6:929133882803122216> **Fetching critterz...**', color = self.bot.color)
        load_message = await ctx.send(embed=embed)    
        try:
            endpoint='https://hasura-dxhfx4osrq-ue.a.run.app/v1/graphql'

            query_owned="""query
                TokensOfOwner($account_address: String!, $_token_address: String!) {
                    \n  tokens_of_owner(\n    args: {account_address: $account_address, _token_address: $_token_address}\n  ) {
                    \n    to_address\n    block_number\n    token_address\n    token_id\n    from_address\n    txn_hash\n    __typename\n  
                }\n
            }"""

            query_rented="""query
                TokensOfRenter($account_address: String!, $_token_address: String!) {
                    \n  tokens_of_renter(\n    args: {account_address: $account_address, _token_address: $_token_address}\n  ) {
                    \n    to_address\n    block_number\n    token_address\n    token_id\n    from_address\n    txn_hash\n    __typename\n  
                }\n
            }"""

            variables_rented=[{'_token_address':"0x47f75E8dD28dF8d6E7c39ccda47026b0DCa99043", 'account_address':wallet}]
            variables_owner=[{'_token_address':"0x8ffb9b504d497e4000967391e70D542b8cC6748A", 'account_address':wallet},
                            {'_token_address':"0x47f75E8dD28dF8d6E7c39ccda47026b0DCa99043", 'account_address':wallet},
                            {'_token_address':"0x3D7F0F28e1d42082e3de70ec4c9d1D59a07AFFb9", 'account_address':wallet},
                            {'_token_address':"0xB81Cf242671eDAE57754B1a061F62Af08B32926A", 'account_address':wallet}]


            owner_data=[]
            for i in variables_owner:
                async with aiohttp.ClientSession() as session:
                    async with session.post(endpoint, json={"query": query_owned, "variables" : i}) as resp:
                        res_owner = await resp.json()     
                        owner_data.append(len(res_owner['data']['tokens_of_owner']))

            rented_data=[]
            for i in variables_rented:
                async with aiohttp.ClientSession() as session:
                    async with session.post(endpoint, json={"query": query_rented, "variables" : i}) as res:
                        res_owner = await res.json()     
                        rented_data.append(len(res_owner['data']['tokens_of_renter']))
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://server-dxhfx4osrq-ue.a.run.app/block/reward/{wallet}') as re:
                    t = await re.json()
        except:
            await load_message.delete()
            await ctx.send('Error: Invalid wallet address')
            return
            
        embed=discord.Embed(color=self.bot.color, title=(f'{wallet[0:5]}...{wallet[37:41]}'), url='https://opensea.io/{}', 
            description='Play Rewards: `{}`\nRental Rewards: `{}`'.format(round(t['playReward'], 2), (t['rentalRewards'] if t['rentalRewards'] != {} else 0))).add_field(
                name='Genesis Critterz', value=f"`{owner_data[0]}`").add_field(
                    name='Staked Critterz', value=f"`{owner_data[1]}`").add_field(
                        name='Rented Critterz', value=f"`{rented_data[0]}`").add_field(
                            name='Plots', value=f"`{owner_data[2]}`").add_field(
                                name='Staked Plots', value=f"`{owner_data[3]}`").add_field(name='\u200B', value='\u200B').set_author(
                                    name="Critterz Stat Checker")
        await load_message.delete()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print('\x1b[6;30;42m' + f'Stats Checker Cog - Online' + '\x1b[0m')

def setup(bot):
    bot.add_cog(stats_checker(bot)) 
