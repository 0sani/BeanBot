# BeanBot
A new general-purpose, local-hosted bot for use in a Discord server. 
Made for the BeanChat server (the greatest server of all time).

## Purpose
- Assign and remove roles
- Perform basic moderation tasks like mute, kick, and ban

## Creators
- Doggo, FearlessDoggo21
- Osani, 0sani

## Documentation
Command Prefix: '?'

mute @member, [reason]=`"No reason given"`, [muted_role_name]=`"Muted"`
Gives a user a specific "Muted" role based on the `muted_role_name` for `reason`. Administrators only. 

unmute @member, [muted_role_name]=`"Muted"`
Removes a specific "Muted" role from a user based on the `muted_role_name`. Administrators only.

kick @member, [reason]=`"No reason given"`
Kicks a user out of the server. Administrators only.

get_role name
Gets a role under the `highest_get_role` in the role hierarchy.

remove_role name
Removes a role under the `highest_get_role` in the role hierarchy.

give_role member, name
Gives a role to a user. Administrators only.

take_role mamber, name
Takes a role from a user. Administrators only.
