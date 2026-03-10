# -*- coding: utf-8 -*-
# @author: 小白
"""
定时任务管理
"""
import asyncio
import datetime
from loguru import logger
from app.db.sqlalchemy import async_session
from app.models.system_models import UserLoginRecord


async def cleanup_login_records():
    """
    清理30天前的登录记录
    """
    try:
        async with async_session() as session:
            # 计算30天前的日期
            thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
            
            # 删除30天前的登录记录
            from sqlalchemy import delete
            stmt = delete(UserLoginRecord).where(
                UserLoginRecord.login_time < thirty_days_ago,
                UserLoginRecord.enabled_flag == 1
            )
            
            result = await session.execute(stmt)
            await session.commit()
            
            logger.info(f"清理了 {result.rowcount} 条30天前的登录记录")
    except Exception as e:
        logger.error(f"清理登录记录失败: {e}")


async def run_scheduled_tasks():
    """
    运行定时任务
    """
    while True:
        # 每天凌晨执行清理任务
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            await cleanup_login_records()
            # 避免重复执行
            await asyncio.sleep(61)
        await asyncio.sleep(60)


if __name__ == "__main__":
    # 测试清理任务
    asyncio.run(cleanup_login_records())