# pvfUtility MCP Server

一个为 pvfUtility 软件提供 MCP (Model Context Protocol) 接口的服务器，支持通过 AI 助手操作 DNF 游戏文件。

## 🚀 快速开始

### 系统要求

- Windows 操作系统
- Python 3.10 或更高版本
- pvfUtility 软件（需要开启 WebApi 服务）
- uv 包管理器（推荐）或 pip

### 安装步骤

1. **安装依赖**
   ```bash
   # 双击运行安装脚本
   install.bat
   
   # 或手动安装
   pip install -r requirements.txt
   ```

2. **测试环境**
   ```bash
   # 测试 uv 环境
   test_uv.bat
   ```

3. **启动服务器**
   ```bash
   # 启动 MCP 服务器
   start_mcp.bat
   ```

### MCP 客户端配置

将以下配置添加到您的 MCP 客户端配置文件中：

```json
{
  "mcpServers": {
    "pvfutility": {
      "command": "uv",
      "args": [
        "run",
        "mcp_server.py",
        "--base-url",
        "http://localhost:27000"
      ],
      "cwd": "path/to/pvfUtility-MCP-Release"
    }
  }
}
```

**注意**: 请将 `"cwd"` 中的 `"path/to/pvfUtility-MCP-Release"` 替换为您实际解压文件的完整路径。

**示例**:
- Windows: `"C:\\Users\\YourName\\Desktop\\pvfUtility-MCP-Release"`
- 相对路径: `"./pvfUtility-MCP-Release"` (如果配置文件在上级目录)

## 📋 功能特性

### 🔧 基础信息
- 获取 pvfUtility 版本信息
- 获取 PVF 根目录列表
- 获取当前加载的 PVF 包文件路径

### 📁 文件操作
- 获取指定目录的文件列表
- 读取文件内容（支持多种编码）
- 检查文件/文件夹存在性
- 删除文件
- 导入/覆盖文件内容

### 🔍 搜索功能
- PVF 文件搜索（支持正则表达式）
- 获取所有 LST 文件列表
- 获取 LST 文件详细信息

### 🎮 游戏数据
- 获取物品信息（代码和名称）
- 物品代码转文件信息
- 获取文件图标
- 获取字符串表数据

### 📦 批量操作
- 批量获取文件内容
- 批量获取物品信息
- 批量删除文件
- 批量导入文件

### 🔧 高级功能
- 获取 JSON 格式的文件数据
- PVF 包另存为功能

## 🛠️ 文件说明

| 文件名 | 说明 |
|--------|------|
| `mcp_server.py` | MCP 服务器主程序 |
| `pyproject.toml` | 项目配置文件 |
| `requirements.txt` | Python 依赖列表 |
| `install.bat` | 自动安装脚本 |
| `start_mcp.bat` | 启动服务器脚本 |
| `test_uv.bat` | 环境测试脚本 |
| `mcp_config.json` | MCP 配置示例 |
| `使用说明.md` | 详细中文使用说明 |

## ⚠️ 重要提示

1. **确保 pvfUtility 软件正在运行**，并且 WebApi 服务已启用
2. **默认端口为 27000**，如需修改请更新配置文件
3. **首次使用前请运行测试脚本**确认环境配置正确
4. **批量操作请谨慎使用**，建议先备份重要数据

## 🔧 故障排除

### 连接失败
- 检查 pvfUtility 软件是否运行
- 确认 WebApi 服务已启用
- 验证端口 27000 是否可用

### 依赖问题
- 运行 `install.bat` 重新安装依赖
- 检查 Python 版本是否符合要求
- 确认 uv 包管理器已正确安装

### 编码问题
- 确保文件使用正确的编码格式
- 中文内容建议使用 UTF-8 编码

## 📞 技术支持

如遇到问题，请检查：
1. pvfUtility 软件版本兼容性
2. Python 环境配置
3. 网络连接状态
4. 防火墙设置

## 📄 许可证

本项目基于 MIT 许可证开源，详见 LICENSE 文件。

---

**版本**: 1.0.0  
**更新日期**: 2025-01-06  
**兼容性**: pvfUtility 1.9.1+, Python 3.10+