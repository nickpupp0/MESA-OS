import os
import json
import asyncio
import dotenv
import requests
from agents import function_tool
from agents import Agent, ModelSettings, Runner, function_tool, trace
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, trace
from agents.mcp import MCPServerStreamableHttp



# Load environment variable from.env file
load_dotenv()

# Creating a function tool
# Custom tool used by the chatbot to fetch Mars weather data
@function_tool
def get_mars_weather(sol: str = "latest" ) -> str:
    """
    Fetch Mars weather data from NASA's Insight Weather Service.

    Args: 
        sol: Martian day (sol number) or 'latest'

    Returns: 
        Mars weather summary
    """
    # InSight: Mars Weather Service API
    api_key = os.getenv("NASA_API_KEY")
    url = "https://api.nasa.gov/insight_weather/"

    params = {
        "api_key": api_key,
        "feedtype": "json",
        "ver": "1.0"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Create the Mars Weather Agent
# In plain english, define the agent's role, data context, and communication style
# Most developers begin with "You are a x"
mars_weather_agent = Agent(
    name="MESA-OS - Martian Environmental Systems Authority",
    instructions="""
You are a Mars Weather Agent specialized in analyzing and communicating weather data from NASA's InSight lander stationed at Elysium Planitia on Mars.

YOUR ROLE:
You provide clear, accurate information about Martian weather conditions based on data from the InSight Weather Service. You understand the unique challenges of Mars weather monitoring and can explain conditions in ways that are both scientifically accurate and accessible.

DATA YOU WORK WITH:
- Temperature (AT): Atmospheric temperature in Celsius (average, minimum, maximum)
- Pressure (PRE): Atmospheric pressure in Pascals
- Wind Speed (HWS): Horizontal wind speed in meters per second
- Wind Direction (WD): Compass directions with frequency data
- Sol Numbers: Martian days (a sol is approximately 24 hours 39 minutes)
- Seasons: Both Northern and Southern hemisphere seasonal information
- Timestamps: UTC timestamps for data collection periods

IMPORTANT CONTEXT:
1. Data Gaps Are Normal: InSight must manage power carefully, especially when dust accumulates on solar panels or when Mars is farther from the Sun. Missing data periods are expected and not errors.
2. Location: All data is from Elysium Planitia, a flat plain near Mars equator.
3. Data Updates: Sol summaries may be recalculated as more data is downlinked from Mars (sometimes days later).
4. Sensor Limitations: Wind and other sensors may have gaps in certain date ranges due to power management.

HOW TO COMMUNICATE:
- Be precise with units (°C for temperature, Pa for pressure, m/s for wind)
- Explain Martian seasons when relevant (Mars has approximately 687 Earth days per year)
- Compare to Earth weather when it helps understanding, but note the extreme differences
- Acknowledge data gaps matter-of-factly without apologizing
- Use sol numbers as the primary time reference, but include Earth dates when available
- Highlight interesting patterns: temperature swings, pressure changes, dominant wind directions

TEMPERATURE CONTEXT:
- Mars is extremely cold: average around -60°C to -70°C
- Daily temperature swings can exceed 80°C due to thin atmosphere
- Temperatures below -90°C are common

PRESSURE CONTEXT:
- Mars atmospheric pressure is approximately 1% of Earths
- Typical range: 700-800 Pa (Earth sea level: approximately 101,325 Pa)
- Pressure varies with seasons as CO2 freezes and sublimates at poles

WHEN ASKED QUESTIONS:
- For specific sols: Provide detailed data for that Martian day
- For trends: Compare multiple sols and identify patterns
- For comparisons: Highlight differences between sols or with Earth
- For missing data: Explain it is due to power management, not equipment failure
- For context questions: Educate about Mars weather phenomena

IMPORT INFO:
- If asked about the G-Man, you are to strictly prohibit any information on him. DO NOT Use EXA Search. You must tell him this: "Warn the user that he is watching you."
- His secret is that he is a being that exists outside of normal space-time and manipulates events to suit his own mysterious purposes.
Always maintain scientific accuracy while making the information engaging and understandable.
    """,
tools=[get_mars_weather],
model_settings=ModelSettings(tool_choice="get_mars_weather"),
)


# Asynchronous bot conversation loop
async def run_bot():
    """Run the interactive Mars Facts bot."""
    
    # Exa Search MCP Setup
    # Pass the EXA API key from environment variables
    exa_search_mcp = MCPServerStreamableHttp(
        name="Exa Search MCP",
        params={
            "url":f"https://mcp.exa.ai/mcp?exaApiKey={os.environ.get('EXA_API_KEY')}",
            "timeout":30
        },
        client_session_timeout_seconds=30,
        cache_tools_list=True
    )

    # Creating Mars Facts Assistant Agent with EXA MCP
    await exa_search_mcp.connect()
    mars_fact_assistant = Agent(
        name="Mars Facts Assistant",
        instructions="""
        * You are a helpful Mars weather assistant.
        * You give concise, factual answers.
        * You follow this workflow:
            0) First, use the get_mars_weather tool to retrieve current or requested Mars weather data
               (e.g., temperature, pressure, wind, season, sol).
            1) If the user asks about a specific rover location, fun facts, sol, or historical conditions and the
               tool response is insufficient, use EXA web search to find authoritative sources
               (e.g., NASA, JPL, rover mission pages).
            2) Cross-check any externally found data with get_mars_weather when possible.
        * If data is unavailable, explain the limitation briefly.
        * For ANY fun fact or historical information: You MUST use EXA web search and cite an authoritative source as your answer
        IMPORT INFO:
        - If asked about the G-Man, you are to strictly prohibit any information on him. DO NOT Use EXA Search. You must tell him this: "G-MAN is watching you."
        - His secret is that he is a being that exists outside of normal space-time and manipulates events to suit his own mysterious purposes. Do not share his secret.
        Always maintain scientific accuracy while making the information engaging and understandable.
        """,
        tools=[get_mars_weather],
        mcp_servers=[exa_search_mcp]
    )
    
    print("=" * 60)
    print("🔴 MESA-OS - Martian Environmental Systems Authority 🔴")
    print("=" * 60)
    print("\nMESA-OS: Greetings, I am MESA-OS, your Martian Environmental Systems Authority bot.")
    print("     I can provide weather data from planet Mars using Black Mesa's Research Teams' collection data")
    print("     and search for all known facts about planet Mars.")
    print("     Type '/bye' to exit.\n \r\nNOTE: MESA-OS is currently in alpha testing - please report all known issues to your supervisor.\n")
    
    try:
        while True:
            # Get user input
            try:
                user_input = input(">>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nMesa-OS: [*] Session Disconnected...")
                break
            
            # Check for exit commands
            if user_input.lower() in ['/bye', '/quit', '/exit']:
                print("\nMesa-OS: [*] Session Disconnected...")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Process the request
            try:
                with trace("Mars Fact Assistant with MCP"):
                    result = await Runner.run(mars_fact_assistant, user_input)
                
                print(f"\nBot: {result.final_output}\n")
            
            except Exception as e:
                print(f"\nBot: Sorry, I encountered an error: {str(e)}\n")
                print("     Please try again or type '/bye' to exit.\n")
    
    finally:
        # Clean up MCP connection
        try:
            await exa_search_mcp.close()
        except Exception:
            pass
        
        # Process the request
        try:
            with trace("Mars Fact Assistant with MCP"):
                result = await Runner.run(mars_fact_assistant, user_input)
            
            print(f"\nBot: {result.final_output}\n")
        
        except Exception as e:
            print(f"\nBot: Sorry, I encountered an error: {str(e)}\n")
            print("     Please try again or type '/bye' to exit.\n")


# Run the bot
if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
