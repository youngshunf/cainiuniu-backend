import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class ApiUsage(Base):
    """API使用记录表"""

    __tablename__ = 'l_api_usage'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='用户ID')
    api_key: Mapped[str] = mapped_column(sa.String(100), index=True, comment='API密钥')
    endpoint: Mapped[str] = mapped_column(sa.String(200), comment='请求端点')
    response_status: Mapped[int] = mapped_column(comment='响应状态码')
    ip_address: Mapped[str] = mapped_column(sa.String(50), comment='IP地址')
    request_params: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='请求参数JSON')
    quota_used: Mapped[int] = mapped_column(default=1, comment='消耗配额')

