import asyncio
import json
from typing import Any, Dict, List, Optional
from pathlib import Path
import PyMuPDF as fitz
import pdfplumber
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
)

class PDFProcessingServer:
    def __init__(self):
        self.server = Server("pdf-processor")
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="extract_text",
                        description="Extract text content from PDF file",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the PDF file"
                                },
                                "method": {
                                    "type": "string",
                                    "enum": ["pymupdf", "pdfplumber", "both"],
                                    "description": "Extraction method to use",
                                    "default": "both"
                                }
                            },
                            "required": ["file_path"]
                        }
                    ),
                    Tool(
                        name="extract_tables",
                        description="Extract tables from PDF file",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the PDF file"
                                },
                                "page_numbers": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "description": "Specific pages to extract tables from"
                                }
                            },
                            "required": ["file_path"]
                        }
                    ),
                    Tool(
                        name="analyze_document_structure",
                        description="Analyze PDF document structure and metadata",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the PDF file"
                                }
                            },
                            "required": ["file_path"]
                        }
                    )
                ]
            )

        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            try:
                if request.name == "extract_text":
                    return await self._extract_text(request.arguments)
                elif request.name == "extract_tables":
                    return await self._extract_tables(request.arguments)
                elif request.name == "analyze_document_structure":
                    return await self._analyze_structure(request.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.name}")
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )

    async def _extract_text(self, args: Dict[str, Any]) -> CallToolResult:
        file_path = args["file_path"]
        method = args.get("method", "both")
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        results = {}
        
        if method in ["pymupdf", "both"]:
            try:
                doc = fitz.open(file_path)
                pymupdf_text = ""
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    pymupdf_text += f"\n--- Page {page_num + 1} ---\n"
                    pymupdf_text += page.get_text()
                doc.close()
                results["pymupdf"] = pymupdf_text
            except Exception as e:
                results["pymupdf_error"] = str(e)
        
        if method in ["pdfplumber", "both"]:
            try:
                with pdfplumber.open(file_path) as pdf:
                    pdfplumber_text = ""
                    for page_num, page in enumerate(pdf.pages):
                        pdfplumber_text += f"\n--- Page {page_num + 1} ---\n"
                        page_text = page.extract_text()
                        if page_text:
                            pdfplumber_text += page_text
                results["pdfplumber"] = pdfplumber_text
            except Exception as e:
                results["pdfplumber_error"] = str(e)
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(results, indent=2))]
        )

    async def _extract_tables(self, args: Dict[str, Any]) -> CallToolResult:
        file_path = args["file_path"]
        page_numbers = args.get("page_numbers")
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        tables = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                pages_to_process = page_numbers if page_numbers else range(len(pdf.pages))
                
                for page_num in pages_to_process:
                    if isinstance(page_num, int) and 0 <= page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        page_tables = page.extract_tables()
                        
                        for table_idx, table in enumerate(page_tables):
                            tables.append({
                                "page": page_num + 1,
                                "table_index": table_idx + 1,
                                "data": table,
                                "rows": len(table),
                                "columns": len(table[0]) if table else 0
                            })
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error extracting tables: {str(e)}")]
            )
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(tables, indent=2))]
        )

    async def _analyze_structure(self, args: Dict[str, Any]) -> CallToolResult:
        file_path = args["file_path"]
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        analysis = {}
        
        try:
            doc = fitz.open(file_path)
            
            analysis["metadata"] = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", "")
            }
            
            analysis["document_info"] = {
                "page_count": doc.page_count,
                "encrypted": doc.is_encrypted,
                "file_size": Path(file_path).stat().st_size
            }
            
            page_info = []
            for page_num in range(min(doc.page_count, 10)):  # Analyze first 10 pages
                page = doc.load_page(page_num)
                rect = page.rect
                
                page_analysis = {
                    "page_number": page_num + 1,
                    "width": rect.width,
                    "height": rect.height,
                    "rotation": page.rotation,
                    "has_images": len(page.get_images()) > 0,
                    "image_count": len(page.get_images()),
                    "text_length": len(page.get_text()),
                }
                
                page_info.append(page_analysis)
            
            analysis["pages"] = page_info
            doc.close()
            
        except Exception as e:
            analysis["error"] = str(e)
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(analysis, indent=2))]
        )

    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="pdf-processor",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )

async def main():
    server = PDFProcessingServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())