import json

from client import build_client, select_provider
from prompts.prompts import build_system_prompt
from schemas.schema import TOOL_MENU
from tools._init__ import TOOL_FUNCTIONS

def run_agent_turn(messages: list, max_turns: int=10)-> str:
    provider=select_provider()
    client=build_client(provider)

    working=[
        {
            "role": "system",
            "content": build_system_prompt(),
        },
        *messages
    ]

    for _ in range(max_turns):
        response=client.chat.completions.create(
            model=provider.model,
            messages=working,
            tools=TOOL_MENU,
            max_tokens=4096
        )

        message=response.choices[0].message

        if not message.tool_calls:
            answer=message.content
            messages.append({"role": "assistant", "content": answer})
            return answer
        
        # Making a tool call
        working.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": json.dumps(call.function.arguments)
                    }
                } for call in message.tool_calls
            ]
        })

        #make tool calls
        for call in message.tool_calls:
            name=call.function.name
            if name not in TOOL_FUNCTIONS:
                result=f"Unknown Tool: {name}"
            else:
                arguments=json.loads(call.function.arguments)
                # making the actual tool call
                tool_result=TOOL_FUNCTIONS[name](**arguments)

            working.append({
                "role": "tool", # role is tool since we are using tool to answer the query
                "content": str(tool_result),
                "tool_call_id": call.id
            })
        
    # This will be triggered if agent loop doesnt end in max_turns
    fallback="Stopped after hitting max_turns without a final answer"
    
    messages.append({
        "role": "assistant",
        "content": fallback
    })

    return fallback
