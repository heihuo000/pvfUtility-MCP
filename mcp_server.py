#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pvfUtility WebApi MCP Server
为pvfUtility软件提供MCP (Model Context Protocol) 接口封装

作者: Assistant
版本: 1.0.0
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, urlencode
import aiohttp
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pvfutility-mcp")

class PvfUtilityMCPServer:
    """pvfUtility WebApi MCP服务器"""
    
    def __init__(self, base_url: str = "http://localhost:27000"):
        """
        初始化MCP服务器
        
        Args:
            base_url: pvfUtility WebApi的基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.server = Server("pvfutility-mcp")
        self.session: Optional[aiohttp.ClientSession] = None
        
        # 注册工具函数
        self._register_tools()
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def _register_tools(self):
        """注册所有MCP工具函数"""
        
        # 基础信息获取工具
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """返回可用的工具列表"""
            return [
                Tool(
                    name="get_version",
                    description="获取pvfUtility版本号",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_file_list",
                    description="获取指定目录的文件列表",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dir_name": {
                                "type": "string",
                                "description": "目录名称，如equipment"
                            },
                            "return_type": {
                                "type": "integer",
                                "description": "返回类型，0或1",
                                "default": 0
                            },
                            "file_type": {
                                "type": "string",
                                "description": "文件后缀名，如.equ",
                                "default": ""
                            }
                        },
                        "required": ["dir_name"]
                    }
                ),
                Tool(
                    name="get_pvf_root_directory",
                    description="获取PVF根目录列表",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_file_content",
                    description="获取文件内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            },
                            "use_compatible_decompiler": {
                                "type": "boolean",
                                "description": "是否使用兼容性反编译器",
                                "default": False
                            },
                            "encoding_type": {
                                "type": "string",
                                "description": "编码类型：TW/CN/KR/JP/UTF8/Unicode",
                                "default": "UTF8"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="get_file_contents_batch",
                    description="批量获取文件内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_list": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "文件路径列表"
                            },
                            "use_compatible_decompiler": {
                                "type": "boolean",
                                "description": "是否使用兼容性反编译器",
                                "default": False
                            },
                            "encoding_type": {
                                "type": "string",
                                "description": "编码类型",
                                "default": "UTF8"
                            }
                        },
                        "required": ["file_list"]
                    }
                ),
                Tool(
                    name="get_file_data_json",
                    description="获取PVF文件内容(JSON格式)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="delete_file",
                    description="删除文件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "要删除的文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="delete_files_batch",
                    description="批量删除文件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "要删除的文件路径列表"
                            }
                        },
                        "required": ["file_paths"]
                    }
                ),
                Tool(
                    name="import_file",
                    description="导入/覆盖文件内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            },
                            "file_content": {
                                "type": "string",
                                "description": "文件内容"
                            }
                        },
                        "required": ["file_path", "file_content"]
                    }
                ),
                Tool(
                    name="import_files_batch",
                    description="批量导入文件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "FilePath": {"type": "string"},
                                        "FileContent": {"type": "string"}
                                    },
                                    "required": ["FilePath", "FileContent"]
                                },
                                "description": "文件列表，包含路径和内容"
                            }
                        },
                        "required": ["files"]
                    }
                ),
                Tool(
                    name="get_item_info",
                    description="获取物品信息(代码和名称)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "物品文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="get_item_infos_batch",
                    description="批量获取物品信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "物品文件路径列表"
                            }
                        },
                        "required": ["file_paths"]
                    }
                ),
                Tool(
                    name="search_pvf",
                    description="搜索PVF文件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "搜索关键词"
                            },
                            "search_folder": {
                                "type": "string",
                                "description": "搜索文件夹",
                                "default": ""
                            },
                            "search_type": {
                                "type": "integer",
                                "description": "搜索类型",
                                "default": 1
                            },
                            "use_regex": {
                                "type": "boolean",
                                "description": "是否使用正则表达式",
                                "default": False
                            }
                        },
                        "required": ["keyword"]
                    }
                ),
                Tool(
                    name="item_code_to_file_info",
                    description="通过物品代码获取文件信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "lst_names": {
                                "type": "string",
                                "description": "LST名称，多个用逗号分隔，如equipment,stackable"
                            },
                            "item_code": {
                                "type": "integer",
                                "description": "物品代码"
                            }
                        },
                        "required": ["lst_names", "item_code"]
                    }
                ),
                Tool(
                    name="item_codes_to_file_infos_batch",
                    description="批量通过物品代码获取文件信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "lst_names": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "LST名称列表"
                            },
                            "item_codes": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "物品代码列表"
                            }
                        },
                        "required": ["lst_names", "item_codes"]
                    }
                ),
                Tool(
                    name="get_file_icon",
                    description="获取文件图标(Base64格式)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="file_exists",
                    description="检查文件是否存在",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="save_as_pvf",
                    description="PVF封包另存为",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "保存路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="get_pvf_pack_file_path",
                    description="获取当前载入的封包文件路径",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_all_lst_file_list",
                    description="获取所有LST文件列表",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_lst_file_info",
                    description="获取LST文件信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "LST文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="get_string_table",
                    description="获取字符串表数据",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="folder_exists",
                    description="检查文件夹是否存在",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "folder_path": {
                                "type": "string",
                                "description": "文件夹路径"
                            }
                        },
                        "required": ["folder_path"]
                    }
                ),
                Tool(
                    name="get_file_contents_batch",
                    description="批量获取文件内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_list": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "文件路径列表"
                            },
                            "use_compatible_decompiler": {
                                "type": "boolean",
                                "description": "是否使用兼容性反编译器",
                                "default": False
                            },
                            "encoding_type": {
                                "type": "string",
                                "description": "编码类型",
                                "default": "UTF8"
                            }
                        },
                        "required": ["file_list"]
                    }
                ),
                Tool(
                    name="get_item_infos_batch",
                    description="批量获取物品信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "物品文件路径列表"
                            }
                        },
                        "required": ["file_paths"]
                    }
                )
            ]
        
        # 工具调用处理器
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
            """处理工具调用"""
            try:
                result = await self._call_api_tool(name, arguments)
                return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            except Exception as e:
                logger.error(f"工具调用失败 {name}: {e}")
                return [types.TextContent(type="text", text=f"错误: {str(e)}")]
    
    async def _call_api_tool(self, tool_name: str, arguments: dict) -> dict:
        """调用对应的API工具"""
        if not self.session:
            raise RuntimeError("HTTP会话未初始化")
        
        # API映射表
        api_mapping = {
            "get_version": ("GET", "/Api/PvfUtiltiy/getVersion", {}),
            "get_file_list": ("GET", "/Api/PvfUtiltiy/GetFileList", {
                "dirName": arguments.get("dir_name"),
                "returnType": arguments.get("return_type", 0),
                "fileType": arguments.get("file_type", "")
            }),
            "get_pvf_root_directory": ("GET", "/Api/PvfUtiltiy/getPvfRootDirectory", {}),
            "get_file_content": ("GET", "/Api/PvfUtiltiy/GetFileContent", {
                "filePath": arguments.get("file_path"),
                "useCompatibleDecompiler": arguments.get("use_compatible_decompiler", False),
                "encodingType": arguments.get("encoding_type", "UTF8")
            }),
            "get_file_data_json": ("GET", "/Api/PvfUtiltiy/getFileData", {
                "filePath": arguments.get("file_path")
            }),
            "delete_file": ("GET", "/Api/PvfUtiltiy/DeleteFile", {
                "filePath": arguments.get("file_path")
            }),
            "import_file": ("POST", "/Api/PvfUtiltiy/ImportFile", {
                "filePath": arguments.get("file_path")
            }, arguments.get("file_content")),
            "get_item_info": ("GET", "/Api/PvfUtiltiy/GetItemInfo", {
                "filePath": arguments.get("file_path")
            }),
            "item_code_to_file_info": ("GET", "/Api/PvfUtiltiy/ItemCodeToFileInfo", {
                "lstNames": arguments.get("lst_names"),
                "itemCode": arguments.get("item_code")
            }),
            "get_file_icon": ("GET", "/Api/PvfUtiltiy/getFileIcon", {
                "filePath": arguments.get("file_path")
            }),
            "file_exists": ("GET", "/Api/PvfUtiltiy/FileIsExists", {
                "filePath": arguments.get("file_path")
            }),
            "save_as_pvf": ("GET", "/Api/PvfUtiltiy/SaveAsPvfFile", {
                "filePath": quote(arguments.get("file_path", ""), safe='')
            }),
            "get_pvf_pack_file_path": ("GET", "/Api/PvfUtiltiy/GetPvfPackFilePath", {}),
            "get_all_lst_file_list": ("GET", "/Api/PvfUtiltiy/GetAllLstFileList", {}),
            "get_lst_file_info": ("GET", "/Api/PvfUtiltiy/getLstFileInfo", {
                "filePath": arguments.get("file_path")
            }),
            "get_string_table": ("GET", "/Api/PvfUtiltiy/getStringTable", {}),
            "folder_exists": ("GET", "/Api/PvfUtiltiy/FolderIsExists", {
                "folderPath": arguments.get("folder_path")
            })
        }
        
        # 处理POST请求的特殊情况
        post_tools = {
            "get_file_contents_batch": {
                "url": "/Api/PvfUtiltiy/GetFileContents",
                "data": {
                    "FileList": arguments.get("file_list", []),
                    "UseCompatibleDecompiler": arguments.get("use_compatible_decompiler", False),
                    "EncodingType": arguments.get("encoding_type", "UTF8")
                }
            },
            "delete_files_batch": {
                "url": "/Api/PvfUtiltiy/DeleteFiles",
                "data": arguments.get("file_paths", [])
            },
            "import_files_batch": {
                "url": "/Api/PvfUtiltiy/ImportFiles",
                "data": arguments.get("files", [])
            },
            "get_item_infos_batch": {
                "url": "/Api/PvfUtiltiy/GetItemInfos",
                "data": arguments.get("file_paths", [])
            },
            "search_pvf": {
                "url": "/Api/PvfUtiltiy/SearchPvf",
                "data": {
                    "SearchFolder": arguments.get("search_folder", ""),
                    "Keyword": arguments.get("keyword"),
                    "Type": arguments.get("search_type", 1),
                    "SourceType": 0,
                    "NormalUsing": 1,
                    "IsStartMatch": False,
                    "SearchResult": None,
                    "ScriptContentSearchMode": 1,
                    "IsUseLikeSearchPath": False,
                    "Trait": False,
                    "UseRegularExpression": arguments.get("use_regex", False),
                    "WholeWordMatch": False,
                    "RemoveOrKeep": 1,
                    "FileTypesString": None,
                    "ScriptContent": "",
                    "ScriptContentStart": "",
                    "ScriptContentStop": ""
                }
            },
            "item_codes_to_file_infos_batch": {
                "url": "/Api/PvfUtiltiy/ItemCodesToFileInfos",
                "data": {
                    "lstNames": arguments.get("lst_names", []),
                    "ItemCodes": arguments.get("item_codes", [])
                }
            }
        }
        
        # 执行API调用
        if tool_name in post_tools:
            # POST请求
            tool_config = post_tools[tool_name]
            url = f"{self.base_url}{tool_config['url']}"
            
            async with self.session.post(url, json=tool_config['data']) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API调用失败: HTTP {response.status}")
                    
        elif tool_name in api_mapping:
            # GET请求
            method, endpoint, params, *body = api_mapping[tool_name]
            
            if method == "GET":
                # 过滤空参数
                filtered_params = {k: v for k, v in params.items() if v is not None and v != ""}
                url = f"{self.base_url}{endpoint}"
                if filtered_params:
                    url += "?" + urlencode(filtered_params)
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"API调用失败: HTTP {response.status}")
                        
            elif method == "POST":
                # POST请求，带文本内容
                filtered_params = {k: v for k, v in params.items() if v is not None and v != ""}
                url = f"{self.base_url}{endpoint}"
                if filtered_params:
                    url += "?" + urlencode(filtered_params)
                
                content = body[0] if body else ""
                async with self.session.post(url, data=content, headers={'Content-Type': 'text/plain'}) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(f"API调用失败: HTTP {response.status}")
        else:
            raise Exception(f"未知的工具: {tool_name}")

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="pvfUtility WebApi MCP服务器")
    parser.add_argument("--base-url", default="http://localhost:27000", 
                       help="pvfUtility WebApi基础URL (默认: http://localhost:27000)")
    args = parser.parse_args()
    
    async with PvfUtilityMCPServer(args.base_url) as mcp_server:
        # 运行MCP服务器
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await mcp_server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="pvfutility-mcp",
                    server_version="1.0.0",
                    capabilities=mcp_server.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

if __name__ == "__main__":
    asyncio.run(main())