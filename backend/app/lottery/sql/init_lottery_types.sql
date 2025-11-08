-- 初始化彩票类型数据

-- 双色球
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('ssq', '双色球', '福彩', 6, 1, '1-33', '1-16', '每周二、四、日21:15', 
        'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq', 
        'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/', 
        NULL, 1, NOW(), NOW());

-- 大乐透
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('dlt', '大乐透', '体彩', 5, 2, '1-35', '1-12', '每周一、三、六20:25', 
        'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85', 
        'https://www.lottery.gov.cn/kj/kjlb.html?dlt', 
        '85', 1, NOW(), NOW());

-- 福彩3D
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('3d', '福彩3D', '福彩', 3, 0, '0-9', NULL, '每日21:15', 
        'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=3d', 
        'https://www.cwl.gov.cn/ygkj/wqkjgg/fc3d/', 
        NULL, 1, NOW(), NOW());

-- 排列三
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('pls', '排列三', '体彩', 3, 0, '0-9', NULL, '每日20:25', 
        'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=35', 
        'https://www.lottery.gov.cn/kj/kjlb.html?pls', 
        '35', 1, NOW(), NOW());

-- 排列五
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('plw', '排列五', '体彩', 5, 0, '0-9', NULL, '每日20:25', 
        'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=350133', 
        'https://www.lottery.gov.cn/kj/kjlb.html?plw', 
        '350133', 1, NOW(), NOW());

-- 七乐彩
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('qlc', '七乐彩', '福彩', 7, 0, '1-30', NULL, '每周一、三、五21:15', 
        'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=qlc', 
        'https://www.cwl.gov.cn/ygkj/wqkjgg/qlc/', 
        NULL, 1, NOW(), NOW());

-- 快乐8
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('kl8', '快乐8', '福彩', 20, 0, '1-80', NULL, '每日21:15', 
        'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=kl8', 
        'https://www.cwl.gov.cn/ygkj/wqkjgg/kl8/', 
        NULL, 1, NOW(), NOW());

-- 七星彩
INSERT INTO l_lottery_type (code, name, category, red_ball_count, blue_ball_count, red_ball_range, blue_ball_range, draw_time, api_url, web_url, game_no, status, created_time, updated_time)
VALUES ('qxc', '七星彩', '体彩', 7, 0, '0-9', NULL, '每周二、五、日20:25', 
        'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=04', 
        'https://www.lottery.gov.cn/kj/kjlb.html?qxc', 
        '04', 1, NOW(), NOW());

