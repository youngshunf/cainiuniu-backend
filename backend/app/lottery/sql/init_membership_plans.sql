-- 初始化会员套餐数据

-- 免费版
INSERT INTO l_membership_plan (name, price, duration_days, features, max_predictions_per_day, max_custom_combinations, can_use_ml_methods, can_use_api, api_quota_per_day, sort_order, status, created_time, updated_time)
VALUES ('免费版', 0.00, 365, 
        '{"basic_analysis": true, "view_predictions": true, "history_data": 30, "method_count": 5}', 
        5, 0, false, false, 0, 1, 1, NOW(), NOW());

-- 专业版
INSERT INTO l_membership_plan (name, price, duration_days, features, max_predictions_per_day, max_custom_combinations, can_use_ml_methods, can_use_api, api_quota_per_day, sort_order, status, created_time, updated_time)
VALUES ('专业版', 99.00, 30, 
        '{"basic_analysis": true, "traditional_analysis": true, "view_predictions": true, "custom_combinations": true, "history_data": 365, "method_count": 19, "export_data": true}', 
        50, 10, false, false, 0, 2, 1, NOW(), NOW());

-- 旗舰版
INSERT INTO l_membership_plan (name, price, duration_days, features, max_predictions_per_day, max_custom_combinations, can_use_ml_methods, can_use_api, api_quota_per_day, sort_order, status, created_time, updated_time)
VALUES ('旗舰版', 299.00, 30, 
        '{"basic_analysis": true, "traditional_analysis": true, "ml_analysis": true, "statistics_analysis": true, "optimization_analysis": true, "view_predictions": true, "custom_combinations": true, "history_data": -1, "method_count": -1, "export_data": true, "priority_support": true, "auto_prediction": true}', 
        1000, -1, true, true, 1000, 3, 1, NOW(), NOW());

-- 企业版
INSERT INTO l_membership_plan (name, price, duration_days, features, max_predictions_per_day, max_custom_combinations, can_use_ml_methods, can_use_api, api_quota_per_day, sort_order, status, created_time, updated_time)
VALUES ('企业版', 999.00, 30, 
        '{"basic_analysis": true, "traditional_analysis": true, "ml_analysis": true, "statistics_analysis": true, "optimization_analysis": true, "view_predictions": true, "custom_combinations": true, "history_data": -1, "method_count": -1, "export_data": true, "priority_support": true, "auto_prediction": true, "api_access": true, "white_label": true, "custom_algorithm": true}', 
        -1, -1, true, true, 10000, 4, 1, NOW(), NOW());

