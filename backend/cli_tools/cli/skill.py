"""技能管理 CLI 命令

提供技能的验证、发布、批量发布功能。
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal

import cappa

from backend.database.db import async_db_session
from backend.cli_tools.cli.common import (
    console,
    print_error,
    print_header,
    print_info,
    print_success,
)
from backend.cli_tools.packager.skill_packager import SkillPackager
from backend.cli_tools.publisher.skill_publisher import SkillPublisher
from backend.cli_tools.validator.skill_validator import SkillValidator


@cappa.command(name='validate', help='验证技能包结构', default_long=True)
@dataclass
class SkillValidate:
    """验证技能包结构是否符合规范"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='技能包目录路径'),
    ]
    
    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.exists():
            raise cappa.Exit(f'目录不存在: {self.path}', code=1)
    
    async def __call__(self) -> None:
        print_header('技能包验证')
        print_info(f'路径: {self.path}')
        console.print()
        
        validator = SkillValidator(self.path)
        result = validator.validate()
        validator.print_result()
        
        if not result.valid:
            raise cappa.Exit(code=1)


@cappa.command(name='publish', help='发布技能到市场', default_long=True)
@dataclass
class SkillPublish:
    """发布技能到市场"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='技能包目录路径'),
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
        print_header('技能发布')
        print_info(f'路径: {self.path}')
        console.print()
        
        # 预览模式
        if self.preview:
            packager = SkillPackager(self.path)
            packager.print_preview()
            return
        
        # 发布
        publisher = SkillPublisher(self.path)
        async with async_db_session.begin() as db:
            result = await publisher.publish(
                db=db,
                bump=self.bump,
                version=self.version,
                changelog=self.changelog,
            )
        
        console.print()
        if result.success:
            print_success(f'技能发布成功!')
            print_success(f'技能 ID: {result.skill_id}')
            print_success(f'版本: {result.version}')
            print_success(f'下载地址: {result.package_url}')
            print_success(f'SHA256: {result.file_hash}')
        else:
            print_error(f'发布失败: {result.error}')
            raise cappa.Exit(code=1)


@cappa.command(name='publish-all', help='批量发布技能', default_long=True)
@dataclass
class SkillPublishAll:
    """批量发布目录下的所有技能"""
    
    directory: Annotated[
        Path,
        cappa.Arg(help='包含多个技能的目录'),
    ]
    bump: Annotated[
        str,
        cappa.Arg(
            short='-b',
            default='patch',
            help='版本递增类型',
        ),
    ] = 'patch'
    changelog: Annotated[
        str | None,
        cappa.Arg(
            short='-c',
            help='版本更新日志（应用于所有技能）',
        ),
    ] = None
    
    def __post_init__(self) -> None:
        self.directory = Path(self.directory).resolve()
        if not self.directory.exists():
            raise cappa.Exit(f'目录不存在: {self.directory}', code=1)
        
        if self.bump not in ('patch', 'minor', 'major'):
            raise cappa.Exit(f'无效的 --bump 类型: {self.bump}', code=1)
    
    async def __call__(self) -> None:
        print_header('批量发布技能')
        print_info(f'目录: {self.directory}')
        print_info(f'版本递增: {self.bump}')
        console.print()
        
        # 查找所有技能目录（包含 config.yaml 的子目录）
        skill_dirs = []
        for subdir in self.directory.iterdir():
            if subdir.is_dir() and (subdir / 'config.yaml').exists():
                skill_dirs.append(subdir)
        
        if not skill_dirs:
            print_error('未找到任何技能目录（需要包含 config.yaml）')
            raise cappa.Exit(code=1)
        
        print_info(f'找到 {len(skill_dirs)} 个技能:')
        for skill_dir in skill_dirs:
            console.print(f'  • {skill_dir.name}')
        console.print()
        
        # 逐个发布
        success_count = 0
        fail_count = 0
        
        async with async_db_session.begin() as db:
            for skill_dir in skill_dirs:
                console.print(f'\n[bold]发布: {skill_dir.name}[/]')
                
                publisher = SkillPublisher(skill_dir)
                result = await publisher.publish(
                    db=db,
                    bump=self.bump,
                    changelog=self.changelog,
                )
                
                if result.success:
                    print_success(f'{skill_dir.name} v{result.version} 发布成功')
                    success_count += 1
                else:
                    print_error(f'{skill_dir.name} 发布失败: {result.error}')
                    fail_count += 1
        
        console.print()
        print_header('批量发布完成')
        print_info(f'成功: {success_count}')
        if fail_count > 0:
            print_error(f'失败: {fail_count}')
            raise cappa.Exit(code=1)


@cappa.command(name='info', help='查看技能包信息', default_long=True)
@dataclass
class SkillInfo:
    """查看技能包的配置信息"""
    
    path: Annotated[
        Path,
        cappa.Arg(help='技能包目录路径'),
    ]
    
    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.exists():
            raise cappa.Exit(f'目录不存在: {self.path}', code=1)
    
    async def __call__(self) -> None:
        print_header('技能包信息')
        
        validator = SkillValidator(self.path)
        result = validator.validate()
        
        if result.valid and validator.config:
            config = validator.config
            console.print(f'  ID:          [cyan]{config.id}[/]')
            console.print(f'  名称:        [cyan]{config.name}[/]')
            console.print(f'  版本:        [cyan]{config.version}[/]')
            console.print(f'  描述:        [cyan]{config.description}[/]')
            console.print(f'  分类:        [cyan]{config.category or "无"}[/]')
            console.print(f'  标签:        [cyan]{config.tags or "无"}[/]')
            console.print(f'  定价:        [cyan]{config.pricing}[/]')
            console.print(f'  作者:        [cyan]{config.author_name}[/]')
            if config.author_email:
                console.print(f'  邮箱:        [cyan]{config.author_email}[/]')
        else:
            validator.print_result()
            raise cappa.Exit(code=1)


@cappa.command(help='技能管理命令')
@dataclass
class Skill:
    """技能管理命令组"""
    
    subcmd: cappa.Subcommands[SkillValidate | SkillPublish | SkillPublishAll | SkillInfo]
