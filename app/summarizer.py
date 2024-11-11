from openai import OpenAI
from flask import current_app

def summarize_content(query, json_content):
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

    prompt = f"""
    Summarize the following JSON content into a more structured and better insight.
    The original search query was: "{query}"

    JSON content:
    {json_content}
    
    When you are provided with a query and a JSON content, analyze both query and JSON content first before creating the insight.
    Provide a concise summary that addresses the original query and highlights the most relevant information from the JSON content.
    Structure the summary with clear sections and bullet points where appropriate.
    In the event where the provided JSON content does not answer the query in any way possible, simply just summarize the content of the JSON
    without answering to the query.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes web content"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        current_app.logger.error(f"Error in GPT: {str(e)}")
        return None