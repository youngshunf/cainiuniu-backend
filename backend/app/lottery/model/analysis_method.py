import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class AnalysisMethod(Base):
    """分析方法表"""

    __tablename__ = 'l_analysis_method'

    id: Mapped[id_key] = mapped_column(init=False)
    code: Mapped[str] = mapped_column(sa.String(50), unique=True, index=True, comment='方法代码')
    name: Mapped[str] = mapped_column(sa.String(100), comment='方法名称')
    category: Mapped[str] = mapped_column(
        sa.String(50), comment='分类(traditional/machine_learning/statistics/optimization)'
    )
    description: Mapped[str] = mapped_column(UniversalText, comment='方法描述')
    algorithm_type: Mapped[str] = mapped_column(sa.String(50), comment='算法类型')
    applicable_lotteries: Mapped[str] = mapped_column(sa.String(200), comment='适用彩种JSON')
    default_params: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='默认参数JSON')
    required_history_count: Mapped[int] = mapped_column(default=30, comment='所需最少历史期数')
    complexity: Mapped[str] = mapped_column(
        sa.String(20), default='low', comment='计算复杂度(low/medium/high)'
    )
    is_premium: Mapped[bool] = mapped_column(default=False, comment='是否高级功能')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1启用)')

