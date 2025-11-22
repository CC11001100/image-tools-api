#!/usr/bin/env python
"""后端启动脚本 - 生产环境配置"""
import uvicorn

if __name__ == "__main__":
    # 生产环境配置：
    # - 禁用reload（开发模式会增加CPU占用）
    # - workers=1（单副本，K8s负责扩展）
    # - access_log=False（减少日志IO，健康检查会产生大量日志）
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=58888,
        workers=1,
        access_log=True,  # 保留访问日志用于监控
        log_level="info"
    )
