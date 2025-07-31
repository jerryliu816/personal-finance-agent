import asyncio
import json
import aiohttp
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
)

class StockDataServer:
    def __init__(self):
        self.server = Server("stock-data")
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_stock_quote",
                        description="Get current stock quote for a symbol",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock symbol (e.g., AAPL, MSFT)"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="get_market_summary",
                        description="Get market summary for major indices",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "indices": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Market indices to get (default: SPY, QQQ, DIA)",
                                    "default": ["SPY", "QQQ", "DIA"]
                                }
                            }
                        }
                    ),
                    Tool(
                        name="calculate_portfolio_value",
                        description="Calculate total portfolio value from holdings",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "holdings": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "symbol": {"type": "string"},
                                            "shares": {"type": "number"}
                                        },
                                        "required": ["symbol", "shares"]
                                    },
                                    "description": "Array of stock holdings with symbol and share count"
                                }
                            },
                            "required": ["holdings"]
                        }
                    )
                ]
            )

        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            try:
                if request.name == "get_stock_quote":
                    return await self._get_stock_quote(request.arguments)
                elif request.name == "get_market_summary":
                    return await self._get_market_summary(request.arguments)
                elif request.name == "calculate_portfolio_value":
                    return await self._calculate_portfolio_value(request.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.name}")
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )

    async def _get_stock_quote(self, args: Dict[str, Any]) -> CallToolResult:
        symbol = args["symbol"].upper()
        
        # Using Alpha Vantage free API (demo function)
        # In production, you'd use a real API key
        try:
            # Simulate stock data (replace with real API call)
            quote_data = await self._fetch_demo_quote(symbol)
            
            result = {
                "symbol": symbol,
                "price": quote_data["price"],
                "change": quote_data["change"],
                "change_percent": quote_data["change_percent"],
                "volume": quote_data["volume"],
                "last_updated": datetime.now().isoformat()
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error fetching quote for {symbol}: {str(e)}")]
            )

    async def _get_market_summary(self, args: Dict[str, Any]) -> CallToolResult:
        indices = args.get("indices", ["SPY", "QQQ", "DIA"])
        
        summary = {}
        
        for index in indices:
            try:
                quote_data = await self._fetch_demo_quote(index)
                summary[index] = {
                    "price": quote_data["price"],
                    "change": quote_data["change"],
                    "change_percent": quote_data["change_percent"]
                }
            except Exception as e:
                summary[index] = {"error": str(e)}
        
        summary["last_updated"] = datetime.now().isoformat()
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(summary, indent=2))]
        )

    async def _calculate_portfolio_value(self, args: Dict[str, Any]) -> CallToolResult:
        holdings = args["holdings"]
        
        portfolio_value = 0.0
        detailed_holdings = []
        
        for holding in holdings:
            symbol = holding["symbol"].upper()
            shares = float(holding["shares"])
            
            try:
                quote_data = await self._fetch_demo_quote(symbol)
                current_price = quote_data["price"]
                position_value = shares * current_price
                portfolio_value += position_value
                
                detailed_holdings.append({
                    "symbol": symbol,
                    "shares": shares,
                    "current_price": current_price,
                    "position_value": position_value,
                    "change_percent": quote_data["change_percent"]
                })
                
            except Exception as e:
                detailed_holdings.append({
                    "symbol": symbol,
                    "shares": shares,
                    "error": str(e)
                })
        
        result = {
            "total_portfolio_value": portfolio_value,
            "holdings": detailed_holdings,
            "calculated_at": datetime.now().isoformat()
        }
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )

    async def _fetch_demo_quote(self, symbol: str) -> Dict[str, Any]:
        # Demo data - replace with real API calls
        import random
        
        base_prices = {
            "AAPL": 175.00,
            "MSFT": 330.00,
            "GOOGL": 125.00,
            "AMZN": 145.00,
            "TSLA": 200.00,
            "SPY": 450.00,
            "QQQ": 380.00,
            "DIA": 340.00
        }
        
        base_price = base_prices.get(symbol, 100.00)
        
        # Simulate price movement
        change_percent = random.uniform(-3.0, 3.0)
        change = base_price * (change_percent / 100)
        current_price = base_price + change
        volume = random.randint(1000000, 10000000)
        
        return {
            "price": round(current_price, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "volume": volume
        }

    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="stock-data",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )

async def main():
    server = StockDataServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())