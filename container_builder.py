import aiohttp
import discord
from typing import Union, Optional, List


class containermessage:
    CONTAINER_TYPE = 17
    TEXT_DISPLAY_TYPE = 10
    SECTION_TYPE = 9
    # flags
    IS_COMPONENTS_V2 = 1 << 15  # 32768
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token # insert discord bot token here
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
    
    async def send(self, channel: Union[discord.TextChannel, discord.Thread, int], content: str, **kwargs) -> Optional[dict]:
        """
        args:
            channel: Discord channel object or channel ID
            content: The message content (supports markdown)
            **kwargs: Additional parameters (mentions, files, etc.)
        
        returns:
            dict: The created message object, or None if failed
        """
        channel_id = channel.id if hasattr(channel, 'id') else channel
        
        payload = {
            "flags": self.IS_COMPONENTS_V2,
            "components": [
                {
                    "type": self.CONTAINER_TYPE,
                    "components": [
                        {
                            "type": self.TEXT_DISPLAY_TYPE,
                            "content": content
                        }
                    ]
                }
            ]
        }
        
        payload.update(kwargs)
        
        url = f"{self.base_url}/channels/{channel_id}/messages"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"❌ Container send failed ({response.status}): {error_text}")
                    return None
    
    async def send_multiple(self, channel: Union[discord.TextChannel, discord.Thread, int], texts: List[str]) -> Optional[dict]:
        """
        args:
            channel: Discord channel object or channel ID
            texts: List of text strings to display
        returns:
            dict: The created message object, or None if failed
        """
        channel_id = channel.id if hasattr(channel, 'id') else channel
        
        text_components = [
            {
                "type": self.TEXT_DISPLAY_TYPE,
                "content": text
            }
            for text in texts
        ]
        
        payload = {
            "flags": self.IS_COMPONENTS_V2,
            "components": [
                {
                    "type": self.CONTAINER_TYPE,
                    "components": text_components
                }
            ]
        }
        
        url = f"{self.base_url}/channels/{channel_id}/messages"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"❌ Container send failed ({response.status}): {error_text}")
                    return None
    
    def build_payload(self, content: str, **kwargs) -> dict:
        """
        build a container payload without sending
        useful for custom modifications before sending
        
        args:
            content: The message content
            **kwargs: Additional parameters
        returns:
            dict: The payload dictionary
        """
        payload = {
            "flags": self.IS_COMPONENTS_V2,
            "components": [
                {
                    "type": self.CONTAINER_TYPE,
                    "components": [
                        {
                            "type": self.TEXT_DISPLAY_TYPE,
                            "content": content
                        }
                    ]
                }
            ]
        }
        payload.update(kwargs)
        return payload

async def send_container(bot_token: str, channel: Union[discord.TextChannel, discord.Thread, int], content: str) -> Optional[dict]:
    """
    Args:
        bot_token: Your Discord bot token
        channel: Discord channel object or channel ID
        content: The message content
    
    Returns:
        dict: The created message object, or None if failed
    """
    container = containermessage(bot_token)
    return await container.send(channel, content)
