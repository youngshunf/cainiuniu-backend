-- LLM 模块初始化数据
-- 适用于 MySQL 和 PostgreSQL

-- =====================================================
-- 速率限制配置
-- =====================================================
INSERT INTO llm_rate_limit_config (name, daily_token_limit, weekly_token_limit, monthly_token_limit, rpm_limit, tpm_limit, enabled, description, created_time)
VALUES
    ('free_tier', 10000, NULL, 100000, 10, 10000, true, '免费套餐', NOW()),
    ('basic_tier', 100000, NULL, 1000000, 30, 50000, true, '基础套餐', NOW()),
    ('pro_tier', 1000000, NULL, 10000000, 60, 100000, true, '专业套餐', NOW()),
    ('enterprise_tier', 10000000, NULL, 100000000, 120, 500000, true, '企业套餐', NOW());

-- =====================================================
-- 模型供应商
-- =====================================================
INSERT INTO llm_model_provider (name, api_base_url, api_key_encrypted, global_rpm_limit, global_tpm_limit, enabled, is_domestic, description, created_time)
VALUES
    ('openai', 'https://api.openai.com/v1', NULL, 60, 100000, true, false, 'OpenAI 官方 API', NOW()),
    ('anthropic', 'https://api.anthropic.com', NULL, 60, 100000, true, false, 'Anthropic Claude API', NOW()),
    ('qwen', 'https://dashscope.aliyuncs.com/compatible-mode/v1', NULL, 60, 100000, true, true, '阿里云通义千问', NOW()),
    ('deepseek', 'https://api.deepseek.com/v1', NULL, 60, 100000, true, true, 'DeepSeek API', NOW()),
    ('zhipu', 'https://open.bigmodel.cn/api/paas/v4', NULL, 60, 100000, true, true, '智谱 AI GLM', NOW()),
    ('moonshot', 'https://api.moonshot.cn/v1', NULL, 60, 100000, true, true, 'Moonshot Kimi', NOW()),
    ('baichuan', 'https://api.baichuan-ai.com/v1', NULL, 60, 100000, true, true, '百川智能', NOW()),
    ('minimax', 'https://api.minimax.chat/v1', NULL, 60, 100000, true, true, 'MiniMax', NOW());

-- =====================================================
-- 模型配置 - OpenAI
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'gpt-4o', 'GPT-4o', 'TEXT', 16384, 128000, true, true, true, 0.0025, 0.01, 60, 100000, 100, true, NOW() FROM llm_model_provider WHERE name = 'openai';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'gpt-4o-mini', 'GPT-4o Mini', 'TEXT', 16384, 128000, true, true, true, 0.00015, 0.0006, 60, 100000, 90, true, NOW() FROM llm_model_provider WHERE name = 'openai';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'gpt-4-turbo', 'GPT-4 Turbo', 'TEXT', 4096, 128000, true, true, true, 0.01, 0.03, 60, 100000, 80, true, NOW() FROM llm_model_provider WHERE name = 'openai';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'gpt-3.5-turbo', 'GPT-3.5 Turbo', 'TEXT', 4096, 16385, true, true, false, 0.0005, 0.0015, 60, 100000, 70, true, NOW() FROM llm_model_provider WHERE name = 'openai';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'o1-preview', 'O1 Preview', 'REASONING', 32768, 128000, true, false, false, 0.015, 0.06, 20, 50000, 95, true, NOW() FROM llm_model_provider WHERE name = 'openai';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'o1-mini', 'O1 Mini', 'REASONING', 65536, 128000, true, false, false, 0.003, 0.012, 30, 80000, 85, true, NOW() FROM llm_model_provider WHERE name = 'openai';

-- =====================================================
-- 模型配置 - Anthropic
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'claude-3-5-sonnet-20241022', 'Claude 3.5 Sonnet', 'TEXT', 8192, 200000, true, true, true, 0.003, 0.015, 60, 100000, 100, true, NOW() FROM llm_model_provider WHERE name = 'anthropic';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'claude-3-opus-20240229', 'Claude 3 Opus', 'TEXT', 4096, 200000, true, true, true, 0.015, 0.075, 30, 50000, 90, true, NOW() FROM llm_model_provider WHERE name = 'anthropic';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'claude-3-5-haiku-20241022', 'Claude 3.5 Haiku', 'TEXT', 8192, 200000, true, true, true, 0.001, 0.005, 60, 100000, 80, true, NOW() FROM llm_model_provider WHERE name = 'anthropic';

-- =====================================================
-- 模型配置 - 阿里云通义千问
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'qwen-turbo', '通义千问 Turbo', 'TEXT', 6000, 8000, true, true, false, 0.0008, 0.002, 60, 100000, 70, true, NOW() FROM llm_model_provider WHERE name = 'qwen';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'qwen-plus', '通义千问 Plus', 'TEXT', 6000, 32000, true, true, false, 0.004, 0.012, 60, 100000, 80, true, NOW() FROM llm_model_provider WHERE name = 'qwen';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'qwen-max', '通义千问 Max', 'TEXT', 8000, 32000, true, true, false, 0.02, 0.06, 30, 50000, 90, true, NOW() FROM llm_model_provider WHERE name = 'qwen';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'qwen-vl-plus', '通义千问 VL Plus', 'VISION', 6000, 32000, true, false, true, 0.008, 0.008, 60, 100000, 75, true, NOW() FROM llm_model_provider WHERE name = 'qwen';

-- =====================================================
-- 模型配置 - DeepSeek
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'deepseek-chat', 'DeepSeek Chat', 'TEXT', 4096, 64000, true, true, false, 0.00014, 0.00028, 60, 100000, 85, true, NOW() FROM llm_model_provider WHERE name = 'deepseek';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'deepseek-coder', 'DeepSeek Coder', 'TEXT', 4096, 64000, true, true, false, 0.00014, 0.00028, 60, 100000, 80, true, NOW() FROM llm_model_provider WHERE name = 'deepseek';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'deepseek-reasoner', 'DeepSeek Reasoner', 'REASONING', 8192, 64000, true, false, false, 0.00055, 0.00219, 30, 50000, 90, true, NOW() FROM llm_model_provider WHERE name = 'deepseek';

-- =====================================================
-- 模型配置 - 智谱 AI
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'glm-4', 'GLM-4', 'TEXT', 4096, 128000, true, true, false, 0.014, 0.014, 60, 100000, 80, true, NOW() FROM llm_model_provider WHERE name = 'zhipu';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'glm-4-flash', 'GLM-4 Flash', 'TEXT', 4096, 128000, true, true, false, 0.0001, 0.0001, 60, 100000, 85, true, NOW() FROM llm_model_provider WHERE name = 'zhipu';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'glm-4v', 'GLM-4V', 'VISION', 4096, 8192, true, false, true, 0.05, 0.05, 30, 50000, 75, true, NOW() FROM llm_model_provider WHERE name = 'zhipu';

-- =====================================================
-- 模型配置 - Moonshot
-- =====================================================
INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'moonshot-v1-8k', 'Moonshot V1 8K', 'TEXT', 4096, 8000, true, true, false, 0.012, 0.012, 60, 100000, 70, true, NOW() FROM llm_model_provider WHERE name = 'moonshot';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'moonshot-v1-32k', 'Moonshot V1 32K', 'TEXT', 4096, 32000, true, true, false, 0.024, 0.024, 60, 100000, 75, true, NOW() FROM llm_model_provider WHERE name = 'moonshot';

INSERT INTO llm_model_config (provider_id, model_name, display_name, model_type, max_tokens, max_context_length, supports_streaming, supports_tools, supports_vision, input_cost_per_1k, output_cost_per_1k, rpm_limit, tpm_limit, priority, enabled, created_time)
SELECT id, 'moonshot-v1-128k', 'Moonshot V1 128K', 'TEXT', 4096, 128000, true, true, false, 0.06, 0.06, 30, 50000, 80, true, NOW() FROM llm_model_provider WHERE name = 'moonshot';

-- =====================================================
-- 模型组
-- =====================================================
INSERT INTO llm_model_group (name, model_type, model_ids, fallback_enabled, retry_count, timeout_seconds, enabled, description, created_time)
VALUES
    ('text_models', 'TEXT', '[]', true, 3, 60, true, '文本生成模型组', NOW()),
    ('reasoning_models', 'REASONING', '[]', true, 3, 120, true, '推理模型组', NOW()),
    ('vision_models', 'VISION', '[]', true, 3, 60, true, '视觉模型组', NOW());
