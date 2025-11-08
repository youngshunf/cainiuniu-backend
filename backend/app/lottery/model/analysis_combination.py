import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class AnalysisCombination(Base):
    """分析组合配置表"""

    __tablename__ = 'l_analysis_combination'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='用户ID(系统组合为0)')
    name: Mapped[str] = mapped_column(sa.String(100), comment='组合名称')
    lottery_code: Mapped[str] = mapped_column(sa.String(20), index=True, comment='适用彩种')
    method_configs: Mapped[str] = mapped_column(
        UniversalText, comment='方法配置JSON:[{"method_id":1,"weight":0.3,"params":{}}]'
    )
    history_periods: Mapped[int] = mapped_column(default=100, comment='历史期数')
    is_auto: Mapped[bool] = mapped_column(default=False, comment='是否自动预测')
    accuracy_rate: Mapped[float | None] = mapped_column(
        sa.Float, default=None, comment='历史准确率'
    )
    use_count: Mapped[int] = mapped_column(default=0, comment='使用次数')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1启用)')

