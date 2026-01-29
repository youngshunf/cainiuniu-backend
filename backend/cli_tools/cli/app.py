"""应用管理 CLI 命令

提供应用的验证、发布功能。
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import cappa

from backend.database.db import async_db_session
from backend.cli_tools.cli.common import (
    console,
    print_error,
    print_header,
    print_info,
    print_success,
)
from backend.cli_tools.packager.app_packager import AppPackager
from backend.cli_tools.publisher.app_publisher import AppPublisher
from backend.cli_tools.validator.app_validator import AppValidator


@cappa.command(name='validate', help='验证应用包结构', default_long=True)
@dataclass
class AppValidate:
    """验证应用包结构是否符合规范"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='应用包目录路径'),
    ]
    
    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.exists():
            raise cappa.Exit(f'目录不存在: {self.path}', code=1)
    
    async def __call__(self) -> None:
        print_header('应用包验证')
        print_info(f'路径: {self.path}')
        console.print()
        
        validator = AppValidator(self.path)
        result = validator.validate()
        validator.print_result()
        
        if not result.valid:
            raise cappa.Exit(code=1)


@cappa.command(name='publish', help='发布应用到市场', default_long=True)
@dataclass
class AppPublish:
    """发布应用到市场"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='应用包目录路径'),
    ]
    bump: Annotated[
        str | None,
        cappa.Arg(
            short='-b',
            help='版本递增类型: patch (1.0.0 -> 1.0.1), minor (1.0.0 -> 1.1.0), major (1.0.0 -> 2.0.0)',
        ),
    ] = None
    version: Annotated[
        str | None,
        cappa.Arg(
            short='-v',
            help='指定版本号（与 --bump 互斥）',
        ),
    ] = None
    changelog: Annotated[
        str | None,
        cappa.Arg(
            short='-c',
            help='版本更新日志',
        ),
    ] = None
    preview: Annotated[
        bool,
        cappa.Arg(
            short='-p',
            default=False,
            help='仅预览将要打包的文件，不执行发布',
        ),
    ] = False
    
    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.exists():
            raise cappa.Exit(f'目录不存在: {self.path}', code=1)
        
        if self.bump and self.version:
            raise cappa.Exit('--bump 和 --version 不能同时使用', code=1)
        
        if self.bump and self.bump not in ('patch', 'minor', 'major'):
            raise cappa.Exit(f'无效的 --bump 类型: {self.bump}，应为 patch/minor/major', code=1)
    
    async def __call__(self) -> None:
        print_header('应用发布')
        print_info(f'路径: {self.path}')
        console.print()
        
        # 预览模式
        if self.preview:
            packager = AppPackager(self.path)
            packager.print_preview()
            return
        
        # 发布
        publisher = AppPublisher(self.path)
        async with async_db_session.begin() as db:
            result = await publisher.publish(
                db=db,
                bump=self.bump,
                version=self.version,
                changelog=self.changelog,
            )
        
        console.print()
        if result.success:
            print_success(f'应用发布成功!')
            print_success(f'应用 ID: {result.app_id}')
            print_success(f'版本: {result.version}')
            print_success(f'下载地址: {result.package_url}')
            print_success(f'SHA256: {result.file_hash}')
        else:
            print_error(f'发布失败: {result.error}')
            raise cappa.Exit(code=1)


@cappa.command(name='info', help='查看应用包信息', default_long=True)
@dataclass
class AppInfo:
    """查看应用包的配置信息"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='应用包目录路径'),
    ]
    
    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.exists():
            raise cappa.Exit(f'目录不存在: {self.path}', code=1)
    
    async def __call__(self) -> None:
        print_header('应用包信息')
        
        validator = AppValidator(self.path)
        result = validator.validate()
        
        if result.valid and validator.manifest:
            manifest = validator.manifest
            console.print(f'  ID:          [cyan]{manifest.id}[/]')
            console.print(f'  名称:        [cyan]{manifest.name}[/]')
            console.print(f'  版本:        [cyan]{manifest.version}[/]')
            console.print(f'  类型:        [cyan]{manifest.app_type}[/]')
            console.print(f'  描述:        [cyan]{manifest.description}[/]')
            console.print(f'  定价:        [cyan]{manifest.pricing_type}[/]')
            console.print(f'  作者:        [cyan]{manifest.author_name}[/]')
            if manifest.author_email:
                console.print(f'  邮箱:        [cyan]{manifest.author_email}[/]')
            if manifest.skill_dependencies:
                console.print(f'  技能依赖:')
                for dep in manifest.skill_dependencies:
                    console.print(f'    • [cyan]{dep}[/]')
        else:
            validator.print_result()
            raise cappa.Exit(code=1)


@cappa.command(help='应用管理命令')
@dataclass
class App:
    """应用管理命令组"""
    
    subcmd: cappa.Subcommands[AppValidate | AppPublish | AppInfo]
