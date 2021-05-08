-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 04, 2021 at 09:58 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jds_main_db`
--
CREATE DATABASE IF NOT EXISTS `jds_main_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `jds_main_db`;

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(12) NOT NULL,
  `app_ID` text NOT NULL,
  `app_name` text NOT NULL,
  `app_desc` text NOT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `applications`:
--

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `app_ID`, `app_name`, `app_desc`, `dateCreated`) VALUES
(1, 'APP_92ASA2_32S0', 'Joint Downloading System', 'A tool that allows users download online contents with friends.', '2020-12-03 23:03:01');

-- --------------------------------------------------------

--
-- Table structure for table `authlogin`
--

CREATE TABLE `authlogin` (
  `id` int(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `deviceKey` text NOT NULL,
  `usr_channel` text DEFAULT NULL,
  `local_net_addr` text DEFAULT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `authlogin`:
--   `user_id`
--       `user` -> `user_id`
--

--
-- Dumping data for table `authlogin`
--

INSERT INTO `authlogin` (`id`, `user_id`, `deviceKey`, `usr_channel`, `local_net_addr`, `dateCreated`) VALUES
(147, 3, '861fa0b40531486db307453b00d36442ccbc1b2b282559c7072f493092ca8881c3e12e65e1725aeb90a1515d2a506b1db676a6cd82af1a77f75554aa2e212e64', NULL, NULL, '2021-02-19 22:26:44'),
(300, 4, '8234acc8525124fd939b7ebd3e3d2f99e0b98fe32913bd1777039d390044a61112d4e09f077163bece07c919f0877f26ef07a8bd812e3c7db63c0e87c7a32a9e', NULL, '[\\\"10.6.8.190\\\",\\\"192.168.52.1\\\",\\\"192.168.232.1\\\",\\\"172.29.160.1\\\"]', '2021-04-30 05:43:40'),
(306, 2, '6303f470fda40588d5341432925694c7f4d7e2ea18438418999457b4e985958479800bd9161734596de28fad6e9df8d90eabfe57ddd9a8eba4354c59ff5ad873', NULL, '[\\\"192.168.232.128\\\"]', '2021-04-30 22:28:49'),
(311, 1, '9cd1ec7b344b3f2fa74d6f0c4c04aa9471d49919ae4d8f35742e670cbc561870ba4be9edac244841085a87c94dd357277896af0c57d3136149456fae9e872120', NULL, '[\\\"10.6.8.190\\\",\\\"192.168.52.1\\\",\\\"192.168.232.1\\\",\\\"172.17.160.1\\\"]', '2021-05-03 10:46:55');

-- --------------------------------------------------------

--
-- Table structure for table `chunk`
--

CREATE TABLE `chunk` (
  `id` int(12) NOT NULL,
  `chunk_order` int(12) NOT NULL,
  `joint_id` varchar(12) CHARACTER SET utf8mb4 NOT NULL,
  `request_id` int(12) NOT NULL,
  `byte_start` text COLLATE utf8mb4_bin NOT NULL,
  `byte_end` text COLLATE utf8mb4_bin NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- RELATIONSHIPS FOR TABLE `chunk`:
--   `request_id`
--       `svr_download_request` -> `request_id`
--   `joint_id`
--       `joint_group` -> `joint_id`
--

--
-- Dumping data for table `chunk`
--

INSERT INTO `chunk` (`id`, `chunk_order`, `joint_id`, `request_id`, `byte_start`, `byte_end`, `date_created`) VALUES
(212, 0, 'YI7C3D', 553, '0', '4920249', '2021-05-01 10:59:22'),
(213, 1, 'YI7C3D', 553, '4920250', '9840497', '2021-05-01 10:59:22'),
(214, 0, 'YI7C3D', 555, '0', '188674', '2021-05-01 11:16:13'),
(215, 1, 'YI7C3D', 555, '188675', '377348', '2021-05-01 11:16:13'),
(216, 2, 'YI7C3D', 555, '377349', '566021', '2021-05-01 11:16:13'),
(217, 3, 'YI7C3D', 555, '566022', '754695', '2021-05-01 11:16:13'),
(218, 4, 'YI7C3D', 555, '754696', '943368', '2021-05-01 11:16:13'),
(219, 0, 'BSKMJF', 556, '0', '6488', '2021-05-03 11:51:25'),
(220, 1, 'BSKMJF', 556, '6489', '12976', '2021-05-03 11:51:25'),
(221, 2, 'BSKMJF', 556, '12977', '19464', '2021-05-03 11:51:25'),
(222, 3, 'BSKMJF', 556, '19465', '25951', '2021-05-03 11:51:25'),
(223, 4, 'BSKMJF', 556, '25952', '32439', '2021-05-03 11:51:25'),
(224, 5, 'BSKMJF', 556, '32440', '38927', '2021-05-03 11:51:25'),
(225, 6, 'BSKMJF', 556, '38928', '45414', '2021-05-03 11:51:25'),
(226, 7, 'BSKMJF', 556, '45415', '51902', '2021-05-03 11:51:25'),
(227, 8, 'BSKMJF', 556, '51903', '58390', '2021-05-03 11:51:25'),
(228, 9, 'BSKMJF', 556, '58391', '64877', '2021-05-03 11:51:25'),
(229, 10, 'BSKMJF', 556, '64878', '71365', '2021-05-03 11:51:25'),
(230, 11, 'BSKMJF', 556, '71366', '77853', '2021-05-03 11:51:25'),
(231, 12, 'BSKMJF', 556, '77854', '84341', '2021-05-03 11:51:25'),
(232, 13, 'BSKMJF', 556, '84342', '90828', '2021-05-03 11:51:25'),
(233, 14, 'BSKMJF', 556, '90829', '97316', '2021-05-03 11:51:25'),
(234, 15, 'BSKMJF', 556, '97317', '103804', '2021-05-03 11:51:25'),
(235, 16, 'BSKMJF', 556, '103805', '110291', '2021-05-03 11:51:25'),
(236, 17, 'BSKMJF', 556, '110292', '116779', '2021-05-03 11:51:25'),
(237, 18, 'BSKMJF', 556, '116780', '123267', '2021-05-03 11:51:25'),
(238, 19, 'BSKMJF', 556, '123268', '129754', '2021-05-03 11:51:25'),
(239, 20, 'BSKMJF', 556, '129755', '136242', '2021-05-03 11:51:25');

-- --------------------------------------------------------

--
-- Table structure for table `chunk_child`
--

CREATE TABLE `chunk_child` (
  `id` int(12) NOT NULL,
  `chunk_id` int(12) NOT NULL,
  `chunk_order` int(12) NOT NULL,
  `byte_start` text NOT NULL,
  `byte_end` text NOT NULL,
  `size` varchar(20) DEFAULT '0',
  `progress` varchar(12) DEFAULT '0',
  `user_id` int(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `chunk_child`:
--   `chunk_id`
--       `chunk` -> `id`
--   `user_id`
--       `user` -> `user_id`
--

--
-- Dumping data for table `chunk_child`
--

INSERT INTO `chunk_child` (`id`, `chunk_id`, `chunk_order`, `byte_start`, `byte_end`, `size`, `progress`, `user_id`) VALUES
(221, 212, 0, '0', '2460125', '2460126', '100', 1),
(222, 212, 1, '2460126', '4920250', '2460125', '100', 2),
(223, 213, 2, '4920251', '7380375', '2460125', '100', 1),
(224, 213, 3, '7380376', '9840500', '2460125', '100', 2),
(225, 214, 0, '0', '94337', '94338', '100', 1),
(226, 214, 1, '94338', '188674', '94337', '100', 2),
(227, 215, 2, '188675', '283011', '94337', '100', 1),
(228, 215, 3, '283012', '377348', '94337', '100', 2),
(229, 216, 4, '377349', '471685', '94337', '100', 1),
(230, 216, 5, '471686', '566022', '94337', '100', 2),
(231, 217, 6, '566023', '660359', '94337', '100', 1),
(232, 217, 7, '660360', '754696', '94337', '100', 2),
(233, 218, 8, '754697', '849033', '94337', '100', 1),
(234, 218, 9, '849034', '943370', '94337', '100', 2),
(235, 219, 0, '0', '6488', '6489', '100', 1),
(236, 220, 1, '6489', '12976', '6488', '100', 1),
(237, 221, 2, '12977', '19464', '6488', '100', 1),
(238, 222, 3, '19465', '25952', '6488', '100', 1),
(239, 223, 4, '25953', '32440', '6488', '100', 1),
(240, 224, 5, '32441', '38928', '6488', '100', 1),
(241, 225, 6, '38929', '45416', '6488', '100', 1),
(242, 226, 7, '45417', '51904', '6488', '100', 1),
(243, 227, 8, '51905', '58392', '6488', '100', 1),
(244, 228, 9, '58393', '64880', '6488', '100', 1),
(245, 229, 10, '64881', '71368', '6488', '100', 1),
(246, 230, 11, '71369', '77856', '6488', '100', 1),
(247, 231, 12, '77857', '84344', '6488', '100', 1),
(248, 232, 13, '84345', '90832', '6488', '100', 1),
(249, 233, 14, '90833', '97320', '6488', '100', 1),
(250, 234, 15, '97321', '103808', '6488', '100', 1),
(251, 235, 16, '103809', '110296', '6488', '100', 1),
(252, 236, 17, '110297', '116784', '6488', '100', 1),
(253, 237, 18, '116785', '123272', '6488', '100', 1),
(254, 238, 19, '123273', '129760', '6488', '100', 1),
(255, 239, 20, '129761', '136248', '271', '100', 1);

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

CREATE TABLE `file` (
  `file_id` int(12) NOT NULL,
  `request_id` int(12) NOT NULL,
  `joint_id` varchar(12) NOT NULL,
  `py_channel` text NOT NULL,
  `server_path` text DEFAULT NULL,
  `size` text DEFAULT NULL,
  `md5_hash` text NOT NULL,
  `sha1_hash` text NOT NULL,
  `sha256_hash` text NOT NULL,
  `progress` double DEFAULT 0,
  `init_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `file`:
--   `joint_id`
--       `joint_group` -> `joint_id`
--   `request_id`
--       `svr_download_request` -> `request_id`
--

--
-- Dumping data for table `file`
--

INSERT INTO `file` (`file_id`, `request_id`, `joint_id`, `py_channel`, `server_path`, `size`, `md5_hash`, `sha1_hash`, `sha256_hash`, `progress`, `init_date`) VALUES
(372, 553, 'YI7C3D', '738250', 'C:/xampp/htdocs/JDS/storage/YI7C3D/553/', '9.38 MB', '10c918b1d01aea85864ee65d9e0c2305', 'afed64ed7a90fed976cf76476432105e722049c8', '8ab080c1406dff77f8897955cf977e9ad779e40ab3a07bc2f8694fbd2fc2be21', 0, '2021-05-01 10:59:19'),
(373, 555, 'YI7C3D', '738250', 'C:/xampp/htdocs/JDS/storage/YI7C3D/555/', '921.26 KB', '6ddce22fc53fb38967d61d1db75255f2', 'f9dff8c8ec3ce45b08b7c926a25feb1bda734c0b', 'e68a5034444cd5dd15733b2f2ab1b5c6ac413374afd0455bb40601aaf4359cb8', 67.07689190651499, '2021-05-01 11:16:07'),
(374, 556, 'BSKMJF', '134905', 'C:/xampp/htdocs/JDS/storage/BSKMJF/556/', '126.71 KB', '379d24f476637c38b995b6ddc98702df', 'ac97af19561272acfa90400312edc2ce9c3834d2', '4e7b11096d23c56b53a7e622aad263897d6a7ddb8dfbe9c4459bda6e1e86c8ea', 0, '2021-05-03 10:51:37'),
(375, 556, 'BSKMJF', '134905', 'C:/xampp/htdocs/JDS/storage/BSKMJF/556/', '126.71 KB', '379d24f476637c38b995b6ddc98702df', 'ac97af19561272acfa90400312edc2ce9c3834d2', '4e7b11096d23c56b53a7e622aad263897d6a7ddb8dfbe9c4459bda6e1e86c8ea', 0, '2021-05-03 11:51:24');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group`
--

CREATE TABLE `joint_group` (
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `py_channel` varchar(12) NOT NULL,
  `access_limit` int(2) NOT NULL DEFAULT 10,
  `expiry_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `date_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `joint_group`:
--   `user_id`
--       `user` -> `user_id`
--

--
-- Dumping data for table `joint_group`
--

INSERT INTO `joint_group` (`joint_id`, `user_id`, `py_channel`, `access_limit`, `expiry_date`, `date_created`) VALUES
('BSKMJF', 1, '134905', 10, '2021-06-02 10:48:16', '2021-05-03 10:48:16'),
('YI7C3D', 1, '738250', 10, '2021-05-31 08:10:04', '2021-05-01 08:10:04');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group_member`
--

CREATE TABLE `joint_group_member` (
  `id` int(12) NOT NULL,
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `joint_role` varchar(20) NOT NULL DEFAULT 'member',
  `date_added` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `joint_group_member`:
--   `joint_id`
--       `joint_group` -> `joint_id`
--   `user_id`
--       `user` -> `user_id`
--

--
-- Dumping data for table `joint_group_member`
--

INSERT INTO `joint_group_member` (`id`, `joint_id`, `user_id`, `joint_role`, `date_added`) VALUES
(447, 'YI7C3D', 1, 'owner', '2021-05-01 08:10:04'),
(448, 'YI7C3D', 2, 'member', '2021-05-01 08:10:31'),
(455, 'BSKMJF', 1, 'owner', '2021-05-03 10:48:16');

-- --------------------------------------------------------

--
-- Table structure for table `svr_download_request`
--

CREATE TABLE `svr_download_request` (
  `request_id` int(12) NOT NULL,
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `url` text NOT NULL,
  `ext` varchar(5) NOT NULL,
  `size` text NOT NULL,
  `bytes` text DEFAULT NULL,
  `max_chunk_size` varchar(11) NOT NULL DEFAULT 'auto',
  `init` int(1) NOT NULL DEFAULT 0 COMMENT '0 = ''Waiting''\r\n1 = ''Initialized''\r\n2 = ''Downloaded''\r\n3 = ''Compressing''\r\n4 = ''Splitting''\r\n5 = ''Chunkified''',
  `request_datetime` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `svr_download_request`:
--   `joint_id`
--       `joint_group` -> `joint_id`
--   `user_id`
--       `user` -> `user_id`
--

--
-- Dumping data for table `svr_download_request`
--

INSERT INTO `svr_download_request` (`request_id`, `joint_id`, `user_id`, `url`, `ext`, `size`, `bytes`, `max_chunk_size`, `init`, `request_datetime`) VALUES
(553, 'YI7C3D', 1, 'https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4', 'mp4', '9.38 MB', '9840497', '50', 4, '2021-05-01 10:58:16'),
(555, 'YI7C3D', 1, 'https://images.unsplash.com/photo-1549740425-5e9ed4d8cd34?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&dl=farshad-rezvanian-Eelegt4hFNc-unsplash.jpg&w=2400', 'jpg&w', '921.26 KB', '943368', 'auto', 4, '2021-05-01 11:15:55'),
(556, 'BSKMJF', 1, 'https://www.google.co.uk/logos/doodles/2020/december-holidays-days-2-30-6753651837108830.3-law.gif', 'gif', '126.71 KB', '129754', '5', 4, '2021-05-03 10:48:16');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(12) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `hash` text NOT NULL,
  `joinedOn` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `user`:
--

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `password`, `hash`, `joinedOn`) VALUES
(1, 'admin', 'admin%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:21'),
(2, 'stephen', 'stevenoosunrinde%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:23'),
(3, 'myMacBook', 'mac%40mail.com', '$2y$10$8fh0wyl4mQ2yzG6qJPqFGePgr6xE26LDUIYwY9lVMyzFlvTzcFg5.', 'uk2ZxXt5ovOR', '2021-02-19 10:17:58'),
(4, 'test', 'test%40mail.com', '$2y$10$tahzeBUdglQEM3coT8HnBOTXgDyXkx/LFh/hp9o8Sqmy55e4qmMiC', 'x6tiwjVvpsJM', '2021-04-30 05:43:26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `authlogin`
--
ALTER TABLE `authlogin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `chunk`
--
ALTER TABLE `chunk`
  ADD PRIMARY KEY (`id`),
  ADD KEY `request_id` (`request_id`),
  ADD KEY `joint_id` (`joint_id`);

--
-- Indexes for table `chunk_child`
--
ALTER TABLE `chunk_child`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chunk_id` (`chunk_id`),
  ADD KEY `chunk_child_ibfk_2` (`user_id`);

--
-- Indexes for table `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`file_id`),
  ADD KEY `file_ibfk_1` (`joint_id`),
  ADD KEY `file_ibfk_2` (`request_id`);

--
-- Indexes for table `joint_group`
--
ALTER TABLE `joint_group`
  ADD PRIMARY KEY (`joint_id`),
  ADD KEY `joint_group_ibfk_1` (`user_id`);

--
-- Indexes for table `joint_group_member`
--
ALTER TABLE `joint_group_member`
  ADD PRIMARY KEY (`id`),
  ADD KEY `joint_group_member_ibfk_1` (`joint_id`),
  ADD KEY `joint_group_member_ibfk_2` (`user_id`);

--
-- Indexes for table `svr_download_request`
--
ALTER TABLE `svr_download_request`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `svr_download_request_ibfk_1` (`joint_id`),
  ADD KEY `svr_download_request_ibfk_2` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `authlogin`
--
ALTER TABLE `authlogin`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=312;

--
-- AUTO_INCREMENT for table `chunk`
--
ALTER TABLE `chunk`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=240;

--
-- AUTO_INCREMENT for table `chunk_child`
--
ALTER TABLE `chunk_child`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=256;

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `file_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=376;

--
-- AUTO_INCREMENT for table `joint_group_member`
--
ALTER TABLE `joint_group_member`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=456;

--
-- AUTO_INCREMENT for table `svr_download_request`
--
ALTER TABLE `svr_download_request`
  MODIFY `request_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=557;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authlogin`
--
ALTER TABLE `authlogin`
  ADD CONSTRAINT `authlogin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `chunk`
--
ALTER TABLE `chunk`
  ADD CONSTRAINT `chunk_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `svr_download_request` (`request_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `chunk_ibfk_2` FOREIGN KEY (`joint_id`) REFERENCES `joint_group` (`joint_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `chunk_child`
--
ALTER TABLE `chunk_child`
  ADD CONSTRAINT `chunk_child_ibfk_1` FOREIGN KEY (`chunk_id`) REFERENCES `chunk` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `chunk_child_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `file`
--
ALTER TABLE `file`
  ADD CONSTRAINT `file_ibfk_1` FOREIGN KEY (`joint_id`) REFERENCES `joint_group` (`joint_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `file_ibfk_2` FOREIGN KEY (`request_id`) REFERENCES `svr_download_request` (`request_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `joint_group`
--
ALTER TABLE `joint_group`
  ADD CONSTRAINT `joint_group_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `joint_group_member`
--
ALTER TABLE `joint_group_member`
  ADD CONSTRAINT `joint_group_member_ibfk_1` FOREIGN KEY (`joint_id`) REFERENCES `joint_group` (`joint_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `joint_group_member_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `svr_download_request`
--
ALTER TABLE `svr_download_request`
  ADD CONSTRAINT `svr_download_request_ibfk_1` FOREIGN KEY (`joint_id`) REFERENCES `joint_group` (`joint_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `svr_download_request_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
