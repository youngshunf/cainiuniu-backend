"""模型供应商 Schema"""

from pydantic import Field

from backend.common.schema import SchemaBase


class ProviderBase(SchemaBase):
    """供应商基础 Schema"""

    name: str = Field(description='供应商名称')
    api_base_url: str | None = Field(default=None, description='API 基础 URL')
    global_rpm_limit: int = Field(default=60, description='全局 RPM 限制')
    global_tpm_limit: int = Field(default=100000, description='全局 TPM 限制')
    enabled: bool = Field(default=True, description='是否启用')
    is_domestic: bool = Field(default=False, description='是否国内供应商')
    description: str | None = Field(default=None, description='描述')


class CreateProviderParam(ProviderBase):
    """创建供应商参数"""

    api_key: str | None = Field(default=None, description='API Key (明文，将被加密存储)')


class UpdateProviderParam(SchemaBase):
    """更新供应商参数"""

    name: str | None = Field(default=None, description='供应商名称')
    api_base_url: str | None = Field(default=None, description='API 基础 URL')
    api_key: str | None = Field(default=None, description='API Key (明文，将被加密存储)')
    global_rpm_limit: int | None = Field(default=None, description='全局 RPM 限制')
    global_tpm_limit: int | None = Field(default=None, description='全局 TPM 限制')
    enabled: bool | None = Field(default=None, description='是否启用')
    is_domestic: bool | None = Field(default=None, description='是否国内供应商')
    description: str | None = Field(default=None, description='描述')


class GetProviderDetail(ProviderBase):
    """供应商详情"""

    id: int
    has_api_key: bool = Field(description='是否已配置 API Key')

    @classmethod
    def from_orm_with_key_check(cls, obj) -> 'GetProviderDetail':
        return cls(
            id=obj.id,
            name=obj.name,
            api_base_url=obj.api_base_url,
            global_rpm_limit=obj.global_rpm_limit,
            global_tpm_limit=obj.global_tpm_limit,
            enabled=obj.enabled,
            is_domestic=obj.is_domestic,
            description=obj.description,
            has_api_key=bool(obj.api_key_encrypted),
        )


class GetProviderList(SchemaBase):
    """供应商列表项"""

    id: int
    name: str
    enabled: bool
    is_domestic: bool
    has_api_key: bool
    description: str | None = None
