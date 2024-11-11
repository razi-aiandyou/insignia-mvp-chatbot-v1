import aiohttp
from flask import current_app

async def send_webhook_to_botpress(content):
    botpress_webhook_url = current_app.config['BOTPRESS_WEBHOOK_URL']

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(botpress_webhook_url, json=content) as response:
                if response.status == 200:
                    current_app.logger.info("Sucessfully sent results to Botpress")
                else:
                    current_app.logger.info(f"Failed to send results to Botpress. Status: {response.status}")
        except Exception as e:
            current_app.logger.error(f"Error sending webhook to Botpress: {str(e)}")