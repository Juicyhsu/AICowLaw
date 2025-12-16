@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
python check_pinecone.py
pause
