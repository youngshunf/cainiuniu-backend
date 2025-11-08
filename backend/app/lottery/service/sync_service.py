"""开奖数据同步服务"""

import json
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.lottery.crud import draw_result_dao, lottery_type_dao
from backend.app.lottery.schema.draw_result import AddDrawResultParam
from backend.common.exception import errors
from backend.common.log import log
from backend.utils.timezone import timezone


class SyncService:
    """数据同步服务"""

    @staticmethod
    async def sync_lottery_data(db: AsyncSession, lottery_code: str, page_size: int = 30) -> dict:
        """
        同步彩票开奖数据

        :param db: 数据库会话
        :param lottery_code: 彩种代码
        :param page_size: 每页数量
        :return: 同步结果
        """
        # 获取彩票类型信息
        lottery_type = await lottery_type_dao.get_by_code(db, lottery_code)
        if not lottery_type:
            raise errors.NotFoundError(msg=f'彩种 {lottery_code} 不存在')

        # 根据类别选择同步方法
        if lottery_type.category == '体彩':
            return await SyncService._sync_sports_lottery(db, lottery_type, page_size)
        else:  # 福彩
            return await SyncService._sync_welfare_lottery(db, lottery_type, page_size)

    @staticmethod
    async def _sync_sports_lottery(db: AsyncSession, lottery_type, page_size: int) -> dict:
        """
        同步体彩数据

        :param db: 数据库会话
        :param lottery_type: 彩票类型
        :param page_size: 每页数量
        :return: 同步结果
        """
        try:
            url = lottery_type.api_url
            params = {
                'gameNo': lottery_type.game_no,
                'provinceId': '0',
                'pageSize': page_size,
                'isVerify': '1',
                'pageNo': '1',
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        log.error(f'体彩API请求失败: {response.status}')
                        return await SyncService._sync_from_web(db, lottery_type)

                    data = await response.json()
                    
                    if data.get('success') and data.get('value'):
                        results = data['value']['list']
                        return await SyncService._process_sports_results(db, lottery_type, results)
                    else:
                        log.error(f'体彩API返回数据异常: {data}')
                        return await SyncService._sync_from_web(db, lottery_type)

        except Exception as e:
            log.error(f'同步体彩数据异常: {e}')
            return await SyncService._sync_from_web(db, lottery_type)

    @staticmethod
    async def _sync_welfare_lottery(db: AsyncSession, lottery_type, page_size: int) -> dict:
        """
        同步福彩数据

        :param db: 数据库会话
        :param lottery_type: 彩票类型
        :param page_size: 每页数量
        :return: 同步结果
        """
        try:
            url = lottery_type.api_url
            params = {
                'name': lottery_type.code,
                'pageNo': '1',
                'pageSize': page_size,
                'systemType': 'PC',
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        log.error(f'福彩API请求失败: {response.status}')
                        return await SyncService._sync_from_web(db, lottery_type)

                    data = await response.json()
                    
                    if data.get('state') == 0 and data.get('result'):
                        results = data['result']
                        return await SyncService._process_welfare_results(db, lottery_type, results)
                    else:
                        log.error(f'福彩API返回数据异常: {data}')
                        return await SyncService._sync_from_web(db, lottery_type)

        except Exception as e:
            log.error(f'同步福彩数据异常: {e}')
            return await SyncService._sync_from_web(db, lottery_type)

    @staticmethod
    async def _process_sports_results(db: AsyncSession, lottery_type, results: list) -> dict:
        """
        处理体彩结果数据

        :param db: 数据库会话
        :param lottery_type: 彩票类型
        :param results: 结果列表
        :return: 处理结果
        """
        success_count = 0
        skip_count = 0
        error_count = 0

        for item in results:
            try:
                period = item.get('lotteryDrawNum')
                draw_date_str = item.get('lotteryDrawTime', '')
                draw_date = datetime.strptime(draw_date_str[:10], '%Y-%m-%d').date() if draw_date_str else timezone.now().date()

                # 检查是否已存在
                existing = await draw_result_dao.get_by_lottery_and_period(db, lottery_type.code, period)
                if existing:
                    skip_count += 1
                    continue

                # 解析号码
                draw_result = item.get('lotteryDrawResult', '')
                red_balls, blue_balls = SyncService._parse_sports_numbers(draw_result, lottery_type.code)

                # 额外信息
                extra_info = {
                    'total_sales': item.get('totalSaleAmount'),
                    'pooling_amount': item.get('poolingAmount'),
                }

                # 保存数据
                draw_param = AddDrawResultParam(
                    lottery_type_id=lottery_type.id,
                    lottery_code=lottery_type.code,
                    period=period,
                    draw_date=draw_date,
                    red_balls=json.dumps(red_balls, ensure_ascii=False),
                    blue_balls=json.dumps(blue_balls, ensure_ascii=False) if blue_balls else None,
                    extra_info=json.dumps(extra_info, ensure_ascii=False),
                    sync_source='api',
                )
                await draw_result_dao.add(db, draw_param)
                await db.commit()
                success_count += 1

            except Exception as e:
                log.error(f'处理体彩数据失败: {e}, item: {item}')
                error_count += 1
                continue

        return {
            'success': True,
            'lottery_code': lottery_type.code,
            'success_count': success_count,
            'skip_count': skip_count,
            'error_count': error_count,
        }

    @staticmethod
    async def _process_welfare_results(db: AsyncSession, lottery_type, results: list) -> dict:
        """
        处理福彩结果数据

        :param db: 数据库会话
        :param lottery_type: 彩票类型
        :param results: 结果列表
        :return: 处理结果
        """
        success_count = 0
        skip_count = 0
        error_count = 0

        for item in results:
            try:
                period = item.get('code')
                draw_date_str = item.get('date', '')
                draw_date = datetime.strptime(draw_date_str, '%Y-%m-%d').date() if draw_date_str else timezone.now().date()

                # 检查是否已存在
                existing = await draw_result_dao.get_by_lottery_and_period(db, lottery_type.code, period)
                if existing:
                    skip_count += 1
                    continue

                # 解析号码
                red = item.get('red', '')
                blue = item.get('blue', '')
                red_balls, blue_balls = SyncService._parse_welfare_numbers(red, blue, lottery_type.code)

                # 额外信息
                extra_info = {
                    'sales': item.get('sales'),
                    'poolmoney': item.get('poolmoney'),
                }

                # 保存数据
                draw_param = AddDrawResultParam(
                    lottery_type_id=lottery_type.id,
                    lottery_code=lottery_type.code,
                    period=period,
                    draw_date=draw_date,
                    red_balls=json.dumps(red_balls, ensure_ascii=False),
                    blue_balls=json.dumps(blue_balls, ensure_ascii=False) if blue_balls else None,
                    extra_info=json.dumps(extra_info, ensure_ascii=False),
                    sync_source='api',
                )
                await draw_result_dao.add(db, draw_param)
                await db.commit()
                success_count += 1

            except Exception as e:
                log.error(f'处理福彩数据失败: {e}, item: {item}')
                error_count += 1
                continue

        return {
            'success': True,
            'lottery_code': lottery_type.code,
            'success_count': success_count,
            'skip_count': skip_count,
            'error_count': error_count,
        }

    @staticmethod
    def _parse_sports_numbers(draw_result: str, lottery_code: str) -> tuple[list, list | None]:
        """
        解析体彩号码

        :param draw_result: 开奖结果字符串
        :param lottery_code: 彩种代码
        :return: (红球列表, 蓝球列表)
        """
        numbers = draw_result.split()
        
        if lottery_code == 'dlt':  # 大乐透: 前5个红球，后2个蓝球
            return numbers[:5], numbers[5:7] if len(numbers) >= 7 else None
        elif lottery_code in ['pls', 'plw', 'qxc']:  # 排列三、排列五、七星彩: 无蓝球
            return numbers, None
        else:
            return numbers, None

    @staticmethod
    def _parse_welfare_numbers(red: str, blue: str, lottery_code: str) -> tuple[list, list | None]:
        """
        解析福彩号码

        :param red: 红球字符串
        :param blue: 蓝球字符串
        :param lottery_code: 彩种代码
        :return: (红球列表, 蓝球列表)
        """
        red_balls = red.split(',') if red else []
        
        if lottery_code == 'ssq':  # 双色球: 有蓝球
            blue_balls = [blue] if blue else None
        elif lottery_code in ['3d', 'qlc', 'kl8']:  # 福彩3D、七乐彩、快乐8: 无蓝球或特殊处理
            blue_balls = None
        else:
            blue_balls = None
        
        return red_balls, blue_balls

    @staticmethod
    async def _sync_from_web(db: AsyncSession, lottery_type) -> dict:
        """
        从网页抓取数据（备用方案）

        :param db: 数据库会话
        :param lottery_type: 彩票类型
        :return: 同步结果
        """
        log.warning(f'启用网页抓取备用方案: {lottery_type.code}')
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(lottery_type.web_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        return {
                            'success': False,
                            'lottery_code': lottery_type.code,
                            'error': '网页访问失败',
                        }

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 这里需要根据实际网页结构解析
                    # 示例代码，实际需要根据网站结构调整
                    # TODO: 实现具体的网页解析逻辑
                    
                    return {
                        'success': False,
                        'lottery_code': lottery_type.code,
                        'error': '网页解析功能待实现',
                    }

        except Exception as e:
            log.error(f'网页抓取失败: {e}')
            return {
                'success': False,
                'lottery_code': lottery_type.code,
                'error': str(e),
            }

    @staticmethod
    async def calculate_next_period(db: AsyncSession, lottery_code: str) -> str:
        """
        计算下期期号

        :param db: 数据库会话
        :param lottery_code: 彩种代码
        :return: 下期期号
        """
        latest = await draw_result_dao.get_latest_by_lottery(db, lottery_code)
        if not latest:
            # 如果没有历史数据，返回默认期号
            return f'{timezone.now().year}001'
        
        try:
            # 解析期号（格式通常为: YYYYNNN，如2025001）
            current_period = latest.period
            year = int(current_period[:4])
            number = int(current_period[4:])
            
            # 跨年处理
            current_year = timezone.now().year
            if year < current_year:
                return f'{current_year}001'
            
            # 下一期
            next_number = number + 1
            return f'{year}{next_number:03d}'
        except Exception as e:
            log.error(f'计算下期期号失败: {e}')
            return f'{timezone.now().year}001'


sync_service = SyncService()

