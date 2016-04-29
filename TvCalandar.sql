-- phpMyAdmin SQL Dump
-- version 4.6.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 29, 2016 at 03:04 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `TvCalandar`
--

-- --------------------------------------------------------

--
-- Table structure for table `budget`
--
-- Creation: Apr 10, 2016 at 07:54 AM
--

CREATE TABLE `budget` (
  `b_id` int(11) NOT NULL,
  `b_kind` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收入或支出',
  `b_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '引起变动的原因',
  `b_amount` float NOT NULL COMMENT '收入为正，支出为负',
  `b_time` date NOT NULL COMMENT '日期'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收支表';

--
-- RELATIONS FOR TABLE `budget`:
--

-- --------------------------------------------------------

--
-- Table structure for table `download_count`
--
-- Creation: Apr 29, 2016 at 06:27 AM
--

CREATE TABLE `download_count` (
  `e_id` int(11) NOT NULL COMMENT '外键于episode的id',
  `count` bigint(20) NOT NULL DEFAULT '0' COMMENT '下载数量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='统计下载数量的表';

--
-- RELATIONS FOR TABLE `download_count`:
--   `e_id`
--       `episode` -> `e_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `episode`
--
-- Creation: Mar 25, 2016 at 02:28 AM
--

CREATE TABLE `episode` (
  `e_id` int(11) NOT NULL COMMENT '主键id',
  `s_id` int(11) NOT NULL COMMENT '外键于剧的id',
  `se_id` int(11) NOT NULL COMMENT '作为索引而不是外键',
  `e_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '集的名称',
  `e_num` int(11) DEFAULT NULL COMMENT '本季的第X集',
  `e_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '集的状态',
  `e_description` text COLLATE utf8mb4_unicode_ci COMMENT '每一集的介绍',
  `e_time` datetime DEFAULT NULL COMMENT '每一集上映时间，精确到具体时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='集表';

--
-- RELATIONS FOR TABLE `episode`:
--   `s_id`
--       `shows` -> `s_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `season`
--
-- Creation: Mar 20, 2016 at 10:35 AM
--

CREATE TABLE `season` (
  `se_id` int(11) NOT NULL COMMENT '季的id',
  `s_id` int(11) NOT NULL COMMENT '外键于show的id',
  `se_num` int(11) NOT NULL COMMENT '第X季',
  `e_count` int(11) DEFAULT NULL COMMENT '每季有X集'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='季表';

--
-- RELATIONS FOR TABLE `season`:
--   `s_id`
--       `shows` -> `s_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `shows`
--
-- Creation: Apr 27, 2016 at 07:57 AM
--

CREATE TABLE `shows` (
  `s_id` int(11) NOT NULL COMMENT '剧的id',
  `s_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '剧名称',
  `s_name_cn` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '中文翻译',
  `s_description` text COLLATE utf8mb4_unicode_ci COMMENT '剧介绍',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '剧的状态',
  `length` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '每集长度',
  `area` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地区',
  `channel` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电视台',
  `s_sibox_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'sibox的小图片url',
  `update_time` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '每周更新时间',
  `link` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '连接去那个子页面',
  `r_id` bigint(11) UNSIGNED DEFAULT NULL COMMENT '资源的resource_id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='剧';

--
-- RELATIONS FOR TABLE `shows`:
--

-- --------------------------------------------------------

--
-- Table structure for table `show_to_tag`
--
-- Creation: Apr 11, 2016 at 06:39 AM
--

CREATE TABLE `show_to_tag` (
  `s_id` int(11) NOT NULL COMMENT '外键于剧id',
  `t_id` int(11) NOT NULL COMMENT '外键于tag的id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='剧和标签关系';

--
-- RELATIONS FOR TABLE `show_to_tag`:
--   `s_id`
--       `shows` -> `s_id`
--   `t_id`
--       `tag` -> `t_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `subscribe`
--
-- Creation: Mar 29, 2016 at 03:15 AM
--

CREATE TABLE `subscribe` (
  `u_id` int(11) NOT NULL COMMENT '外键于用户id',
  `s_id` int(11) NOT NULL COMMENT '外键于剧id',
  `sub_time` datetime NOT NULL COMMENT '订阅时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订阅剧';

--
-- RELATIONS FOR TABLE `subscribe`:
--   `s_id`
--       `shows` -> `s_id`
--   `u_id`
--       `user` -> `u_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `synchron`
--
-- Creation: Mar 29, 2016 at 03:17 AM
--

CREATE TABLE `synchron` (
  `u_id` int(11) NOT NULL COMMENT '外键于用户id',
  `e_id` int(11) NOT NULL COMMENT '外键于集id',
  `syn_time` datetime NOT NULL COMMENT '同步时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户同步集';

--
-- RELATIONS FOR TABLE `synchron`:
--   `e_id`
--       `episode` -> `e_id`
--   `u_id`
--       `user` -> `u_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--
-- Creation: Apr 11, 2016 at 06:24 AM
--

CREATE TABLE `tag` (
  `t_id` int(11) NOT NULL COMMENT '标签主键',
  `t_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标签英文名称',
  `t_name_cn` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标签中文名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- RELATIONS FOR TABLE `tag`:
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--
-- Creation: Apr 26, 2016 at 07:17 AM
--

CREATE TABLE `user` (
  `u_id` int(11) NOT NULL COMMENT '用户id',
  `u_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户昵称，如空则用手机号',
  `u_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户手机号，客户端要求必填',
  `u_passwd` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码的哈希',
  `u_token` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '客户端令牌哈希',
  `u_status` int(11) NOT NULL DEFAULT '1' COMMENT '1为可用，其他状态待确认'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户';

--
-- RELATIONS FOR TABLE `user`:
--

-- --------------------------------------------------------

--
-- Table structure for table `user_to_tag`
--
-- Creation: Apr 11, 2016 at 06:41 AM
--

CREATE TABLE `user_to_tag` (
  `u_id` int(11) NOT NULL COMMENT '外键于用户id',
  `t_id` int(11) NOT NULL COMMENT '外键于标签id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户标签关系';

--
-- RELATIONS FOR TABLE `user_to_tag`:
--   `t_id`
--       `tag` -> `t_id`
--   `u_id`
--       `user` -> `u_id`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `budget`
--
ALTER TABLE `budget`
  ADD PRIMARY KEY (`b_id`);

--
-- Indexes for table `download_count`
--
ALTER TABLE `download_count`
  ADD PRIMARY KEY (`e_id`);

--
-- Indexes for table `episode`
--
ALTER TABLE `episode`
  ADD PRIMARY KEY (`e_id`),
  ADD KEY `FK_episode_TO_shows` (`s_id`),
  ADD KEY `FK_episode_TO_season` (`se_id`);

--
-- Indexes for table `season`
--
ALTER TABLE `season`
  ADD PRIMARY KEY (`se_id`),
  ADD KEY `FK_season_TO_shows` (`s_id`);

--
-- Indexes for table `shows`
--
ALTER TABLE `shows`
  ADD PRIMARY KEY (`s_id`),
  ADD KEY `s_name` (`s_name`(191));

--
-- Indexes for table `show_to_tag`
--
ALTER TABLE `show_to_tag`
  ADD PRIMARY KEY (`s_id`,`t_id`),
  ADD KEY `FK_StT_to_tag` (`t_id`);

--
-- Indexes for table `subscribe`
--
ALTER TABLE `subscribe`
  ADD PRIMARY KEY (`u_id`,`s_id`),
  ADD KEY `FK_subscribe_to_shows` (`s_id`);

--
-- Indexes for table `synchron`
--
ALTER TABLE `synchron`
  ADD PRIMARY KEY (`u_id`,`e_id`),
  ADD KEY `FK_synchron_to_episode` (`e_id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`t_id`),
  ADD KEY `t_name` (`t_name`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`u_id`);

--
-- Indexes for table `user_to_tag`
--
ALTER TABLE `user_to_tag`
  ADD PRIMARY KEY (`u_id`,`t_id`),
  ADD KEY `FK_StT_to_tag2` (`t_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `budget`
--
ALTER TABLE `budget`
  MODIFY `b_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `episode`
--
ALTER TABLE `episode`
  MODIFY `e_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id', AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `season`
--
ALTER TABLE `season`
  MODIFY `se_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '季的id';
--
-- AUTO_INCREMENT for table `shows`
--
ALTER TABLE `shows`
  MODIFY `s_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '剧的id', AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `t_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标签主键', AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `u_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id', AUTO_INCREMENT=1;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `download_count`
--
ALTER TABLE `download_count`
  ADD CONSTRAINT `FK_down_to_episode` FOREIGN KEY (`e_id`) REFERENCES `episode` (`e_id`);

--
-- Constraints for table `episode`
--
ALTER TABLE `episode`
  ADD CONSTRAINT `FK_episode_TO_shows` FOREIGN KEY (`s_id`) REFERENCES `shows` (`s_id`);

--
-- Constraints for table `season`
--
ALTER TABLE `season`
  ADD CONSTRAINT `FK_season_TO_shows` FOREIGN KEY (`s_id`) REFERENCES `shows` (`s_id`);

--
-- Constraints for table `show_to_tag`
--
ALTER TABLE `show_to_tag`
  ADD CONSTRAINT `FK_StT_to_shows` FOREIGN KEY (`s_id`) REFERENCES `shows` (`s_id`),
  ADD CONSTRAINT `FK_StT_to_tag` FOREIGN KEY (`t_id`) REFERENCES `tag` (`t_id`);

--
-- Constraints for table `subscribe`
--
ALTER TABLE `subscribe`
  ADD CONSTRAINT `FK_subscribe_to_shows` FOREIGN KEY (`s_id`) REFERENCES `shows` (`s_id`),
  ADD CONSTRAINT `FK_subscribe_to_user` FOREIGN KEY (`u_id`) REFERENCES `user` (`u_id`);

--
-- Constraints for table `synchron`
--
ALTER TABLE `synchron`
  ADD CONSTRAINT `FK_synchron_to_episode` FOREIGN KEY (`e_id`) REFERENCES `episode` (`e_id`),
  ADD CONSTRAINT `FK_synchron_to_user` FOREIGN KEY (`u_id`) REFERENCES `user` (`u_id`);

--
-- Constraints for table `user_to_tag`
--
ALTER TABLE `user_to_tag`
  ADD CONSTRAINT `FK_StT_to_tag2` FOREIGN KEY (`t_id`) REFERENCES `tag` (`t_id`),
  ADD CONSTRAINT `FK_StT_to_user` FOREIGN KEY (`u_id`) REFERENCES `user` (`u_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
