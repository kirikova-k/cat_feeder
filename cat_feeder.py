import asyncio
from dotenv import find_dotenv, load_dotenv
from langchain_gigachat import GigaChat
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich import print as rprint

model = GigaChat(model="GigaChat-2-Max",
                credentials="",
                verify_ssl_certs=False,
                streaming=False,
                max_tokens=8000,
                timeout=600)

#копипаст логгера из гайда
def _log(ans):
    for message in ans['messages']:
        rprint(f"[{type(message).__name__}] {message.content} {getattr(message, 'tool_calls', '')}")


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"], #название файла с тулзами
    )

    async with stdio_client(server_params) as (read, write):
        #I/O коннект
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            prompt="Ты - ассистент по кормлению кота. Пользователь вводит вес кота. Если вес больше 5 ты гладишь кота" \
            "Если вес меньше 5 ты кормишь кота. Если вес некорректный нужно сообщить об ошибке"

            #TODO: deprecated метод
            agent = create_react_agent(model=model, tools=tools, prompt=prompt)
            while True:
                user_input = input("Вес кота: ")
                if user_input.lower() == "exit":
                    break    
                #отправка сообщения ии агенту, agent_response - ответ
                agent_response = await agent.ainvoke({"messages": [
                    {"role": "user", "content": "Вес кота:" + user_input}]})
                _log(agent_response)
            
# Run the main function
asyncio.run(main())
