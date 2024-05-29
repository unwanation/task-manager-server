from g4f.client import Client

from models.ai_response_model import AIResponseModel

BASE_PROMPT = (
    'You are an interpreter, which converts natural language to tasks. Response schema: {"tasks": array of Tasks}. '
    'Task schema: {"name": string, '
    '"priority": int (1 - high, 3 - low), "deadline": seconds (3600 in an hour, 86400 in a day)}. Return response '
    "in JSON. "
    "Request="
)

client = Client()


def ai_request(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": BASE_PROMPT + prompt,
            },
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def ai_parse(prompt: str, try_count=0) -> AIResponseModel:
    try_count += 1
    try:
        response = ai_request(prompt)
        return AIResponseModel.model_validate_json(response)
    except:
        if try_count < 10:
            return ai_parse(prompt, try_count)
        else:
            raise Exception("Failed to parse AI response")
