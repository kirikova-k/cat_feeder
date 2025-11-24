from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import sys

mcp = FastMCP("CatFeeder")

class Query(BaseModel):
    query: str

@mcp.tool()
def feed_cat(weight: float) -> float:
    """Feed Cat"""
    print(f">>> Feeding cat {weight} food")
    return weight + 0.3

@mcp.tool()
def pet_cat():
    """Pet cat"""
    return "Pet cat"
if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    mcp.run(transport=transport)