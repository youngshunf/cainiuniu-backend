-- 初始化分析方法数据

-- 传统分析方法 (Traditional Analysis Methods)

-- 1. 频率分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('frequency', '频率分析', 'traditional', '统计每个号码的出现次数和概率，识别高频和低频号码', 'statistical', 
        '["ssq","dlt","3d","pls","plw","qlc","kl8","qxc"]', 
        '{"top_n": 10}', 30, 'low', false, 1, NOW(), NOW());

-- 2. 冷热号分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('hot_cold', '冷热号分析', 'traditional', '识别近期热门号码和冷门号码的分布规律', 'statistical', 
        '["ssq","dlt","3d","pls","plw","qlc","kl8","qxc"]', 
        '{"recent_periods": 20, "hot_threshold": 5}', 20, 'low', false, 1, NOW(), NOW());

-- 3. 大小号分布
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('size_distribution', '大小号分布', 'traditional', '分析大小号码的平衡性和分布规律', 'statistical', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"size_threshold": 0.5}', 30, 'low', false, 1, NOW(), NOW());

-- 4. 和值分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('sum_value', '和值分析', 'traditional', '计算号码和值的分布规律和走势趋势', 'statistical', 
        '["ssq","dlt","3d","pls","plw","qlc","qxc"]', 
        '{"range_count": 10}', 50, 'low', false, 1, NOW(), NOW());

-- 5. 间隔分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('interval', '间隔分析', 'traditional', '研究号码间距的统计特征和规律', 'statistical', 
        '["ssq","dlt","qlc"]', 
        '{}', 50, 'medium', false, 1, NOW(), NOW());

-- 6. 奇偶分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('odd_even', '奇偶分析', 'traditional', '统计奇偶号码的分布规律和比例趋势', 'statistical', 
        '["ssq","dlt","3d","pls","plw","qlc","kl8","qxc"]', 
        '{}', 30, 'low', false, 1, NOW(), NOW());

-- 7. 质合分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('prime_composite', '质合分析', 'traditional', '区分质数和合数的出现规律，分析质合比例的周期性变化', 'mathematical', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 30, 'low', false, 1, NOW(), NOW());

-- 8. 012路分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('road_012', '012路分析', 'traditional', '将号码按除3余数分为0路、1路、2路，分析三路号码的分布平衡性', 'mathematical', 
        '["ssq","dlt","3d","pls","plw","qlc","qxc"]', 
        '{}', 30, 'low', false, 1, NOW(), NOW());

-- 9. AC值分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('ac_value', 'AC值分析', 'traditional', '计算号码的算术复杂性指标，分析AC值的分布规律和趋势', 'mathematical', 
        '["ssq","dlt","qlc"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 10. 跨度分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('span', '跨度分析', 'traditional', '计算最大号码与最小号码的差值，分析跨度的历史分布特征', 'statistical', 
        '["ssq","dlt","qlc"]', 
        '{}', 50, 'low', false, 1, NOW(), NOW());

-- 11. 连号分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('consecutive', '连号分析', 'traditional', '统计连续号码的出现频率和规律性', 'pattern', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 12. 重号分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('repeat', '重号分析', 'traditional', '统计上期号码在本期重复出现的规律和周期性特征', 'pattern', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 13. 邻号分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('adjacent', '邻号分析', 'traditional', '分析相邻号码的关联性和组合规律', 'pattern', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 14. 同尾号分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('same_tail', '同尾号分析', 'traditional', '统计相同尾数号码的分布和出现规律', 'pattern', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 15. 区间分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('zone', '区间分析', 'traditional', '将号码池划分为多个区间，分析各区间号码的分布均衡性', 'statistical', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"zone_count": 3}', 50, 'medium', true, 1, NOW(), NOW());

-- 16. 遗漏值分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('omission', '遗漏值分析', 'traditional', '统计每个号码距离上次出现的期数，分析最大遗漏、平均遗漏等指标', 'statistical', 
        '["ssq","dlt","3d","pls","plw","qlc","kl8","qxc"]', 
        '{}', 100, 'medium', true, 1, NOW(), NOW());

-- 17. 尾数和值分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('tail_sum', '尾数和值分析', 'traditional', '计算号码尾数的和值分布和走势规律', 'mathematical', 
        '["ssq","dlt","qlc"]', 
        '{}', 50, 'medium', true, 1, NOW(), NOW());

-- 18. 号码和分布
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('number_sum', '号码和分布', 'traditional', '分析任意两个号码之和的分布，识别高频出现的和值组合', 'mathematical', 
        '["ssq","dlt","qlc"]', 
        '{}', 100, 'high', true, 1, NOW(), NOW());

-- 19. 三分区分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('three_zone', '三分区分析', 'traditional', '将号码分为前、中、后三区，分析各区的出号规律和平衡性', 'statistical', 
        '["ssq","dlt","qlc","kl8"]', 
        '{}', 50, 'low', false, 1, NOW(), NOW());

-- 机器学习方法 (Machine Learning Methods) - 标记为高级功能

-- 20. LSTM时间序列预测
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('lstm', 'LSTM神经网络', 'machine_learning', '使用长短期记忆网络预测号码趋势和序列模式', 'deep_learning', 
        '["ssq","dlt","qlc"]', 
        '{"epochs": 50, "batch_size": 32, "units": 64}', 200, 'high', true, 1, NOW(), NOW());

-- 21. CNN模式识别
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('cnn', 'CNN卷积网络', 'machine_learning', '使用卷积神经网络识别号码出现的模式和特征', 'deep_learning', 
        '["ssq","dlt","qlc"]', 
        '{"epochs": 50, "filters": 32}', 200, 'high', true, 1, NOW(), NOW());

-- 22. 聚类分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('clustering', '聚类分析', 'machine_learning', 'K-means聚类发现号码模式，识别异常组合', 'clustering', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"n_clusters": 5, "algorithm": "kmeans"}', 100, 'medium', true, 1, NOW(), NOW());

-- 23. 关联规则挖掘
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('association', '关联规则挖掘', 'machine_learning', '使用Apriori算法发现号码之间的关联规则和频繁项集', 'association', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"min_support": 0.1, "min_confidence": 0.5}', 100, 'medium', true, 1, NOW(), NOW());

-- 统计学方法 (Statistics Methods)

-- 24. 线性回归
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('linear_regression', '线性回归分析', 'statistics', '使用线性回归分析号码趋势和相关性', 'regression', 
        '["ssq","dlt","qlc"]', 
        '{}', 100, 'medium', true, 1, NOW(), NOW());

-- 25. 马尔可夫链
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('markov_chain', '马尔可夫链分析', 'statistics', '建立号码转移概率矩阵，分析号码状态转换规律', 'markov', 
        '["ssq","dlt","3d","pls","plw","qlc","qxc"]', 
        '{"order": 1}', 150, 'high', true, 1, NOW(), NOW());

-- 26. 贝叶斯分析
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('bayesian', '贝叶斯分析', 'statistics', '使用贝叶斯网络建模号码关系，进行条件概率预测', 'bayesian', 
        '["ssq","dlt","qlc"]', 
        '{}', 100, 'high', true, 1, NOW(), NOW());

-- 27. 蒙特卡洛模拟
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('monte_carlo', '蒙特卡洛模拟', 'statistics', '通过随机模拟进行号码组合预测和风险评估', 'simulation', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"simulations": 10000}', 100, 'high', true, 1, NOW(), NOW());

-- 组合优化方法 (Optimization Methods)

-- 28. 遗传算法
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('genetic', '遗传算法', 'optimization', '使用进化计算优化号码组合，搜索最优解', 'genetic', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"population_size": 100, "generations": 50, "mutation_rate": 0.1}', 100, 'high', true, 1, NOW(), NOW());

-- 29. 粒子群优化
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('pso', '粒子群优化', 'optimization', '使用群体智能搜索最优号码组合', 'particle_swarm', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"particles": 50, "iterations": 100}', 100, 'high', true, 1, NOW(), NOW());

-- 30. 模拟退火算法
INSERT INTO l_analysis_method (code, name, category, description, algorithm_type, applicable_lotteries, default_params, required_history_count, complexity, is_premium, status, created_time, updated_time)
VALUES ('simulated_annealing', '模拟退火算法', 'optimization', '使用概率接受劣解机制避免局部最优，搜索全局最优组合', 'annealing', 
        '["ssq","dlt","qlc","kl8"]', 
        '{"initial_temp": 100, "cooling_rate": 0.95, "iterations": 1000}', 100, 'high', true, 1, NOW(), NOW());

