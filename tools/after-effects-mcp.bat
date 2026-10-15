@echo off
chcp 65001 >nul
set "AE_MCP_DATA_DIR=C:\Users\timur\Videos\AI-Video-Editing\work\.ae-mcp"
"C:\Program Files\nodejs\node.exe" "%~dp0after-effects-mcp\dist\index.js" %*
