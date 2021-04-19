-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2021 at 04:14 AM
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

DROP TABLE IF EXISTS `applications`;
CREATE TABLE `applications` (
  `id` int(12) NOT NULL,
  `app_ID` text NOT NULL,
  `app_name` text NOT NULL,
  `app_desc` text NOT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `app_ID`, `app_name`, `app_desc`, `dateCreated`) VALUES
(1, 'APP_92ASA2_32S0', 'Joint Downloading System', 'A tool that allows users download online contents with friends.', '2020-12-03 23:03:01');

-- --------------------------------------------------------

--
-- Table structure for table `authlogin`
--

DROP TABLE IF EXISTS `authlogin`;
CREATE TABLE `authlogin` (
  `id` int(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `deviceKey` text NOT NULL,
  `usr_channel` text DEFAULT NULL,
  `local_net_addr` text DEFAULT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `authlogin`
--

INSERT INTO `authlogin` (`id`, `user_id`, `deviceKey`, `usr_channel`, `local_net_addr`, `dateCreated`) VALUES
(147, 3, '861fa0b40531486db307453b00d36442ccbc1b2b282559c7072f493092ca8881c3e12e65e1725aeb90a1515d2a506b1db676a6cd82af1a77f75554aa2e212e64', NULL, NULL, '2021-02-19 22:26:44'),
(283, 1, '4fb144264f91479a822e82a98248f40e3eb114dd8a2fc438aa6e985b883d0b6fcfd31c6b41d2694f84100ddb3711b2089b361197c0983455aead01650d6ff3cf', NULL, NULL, '2021-04-18 09:55:37'),
(285, 2, 'f260bfdb37c24614f2b9ab902d2b244b6e4e21a5df969dd38317c219dc0609913e62765e939aa8122b230fefc5c22e22778677d0d307144d09c676518f7e2ded', NULL, '[\\\"172.23.144.1\\\",\\\"10.6.8.190\\\",\\\"192.168.52.1\\\",\\\"192.168.232.1\\\"]', '2021-04-18 22:42:28');

-- --------------------------------------------------------

--
-- Table structure for table `chunk`
--

DROP TABLE IF EXISTS `chunk`;
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
-- Dumping data for table `chunk`
--

INSERT INTO `chunk` (`id`, `chunk_order`, `joint_id`, `request_id`, `byte_start`, `byte_end`, `date_created`) VALUES
(87, 0, 'MNX0K1', 520, '0', '73126960', '2021-04-18 22:44:28'),
(88, 1, 'MNX0K1', 520, '73126960', '146253920', '2021-04-18 22:44:28'),
(89, 2, 'MNX0K1', 520, '146253920', '219380880', '2021-04-18 22:44:28'),
(90, 3, 'MNX0K1', 520, '219380880', '292507840', '2021-04-18 22:44:28'),
(91, 4, 'MNX0K1', 520, '292507840', '365634800', '2021-04-18 22:44:28'),
(92, 0, '9BSW1Y', 521, '0', '73126960', '2021-04-19 00:36:31'),
(93, 1, '9BSW1Y', 521, '73126960', '146253920', '2021-04-19 00:36:31'),
(94, 2, '9BSW1Y', 521, '146253920', '219380880', '2021-04-19 00:36:31'),
(95, 3, '9BSW1Y', 521, '219380880', '292507840', '2021-04-19 00:36:31'),
(96, 4, '9BSW1Y', 521, '292507840', '365634800', '2021-04-19 00:36:31');

-- --------------------------------------------------------

--
-- Table structure for table `chunk_child`
--

DROP TABLE IF EXISTS `chunk_child`;
CREATE TABLE `chunk_child` (
  `id` int(12) NOT NULL,
  `chunk_id` int(12) NOT NULL,
  `chunk_order` int(12) NOT NULL,
  `byte_start` text NOT NULL,
  `byte_end` text NOT NULL,
  `progress` varchar(12) DEFAULT NULL,
  `user_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chunk_child`
--

INSERT INTO `chunk_child` (`id`, `chunk_id`, `chunk_order`, `byte_start`, `byte_end`, `progress`, `user_id`) VALUES
(11, 87, 0, '0', '73126960', NULL, 2),
(12, 88, 1, '73126960', '146253920', NULL, 2),
(13, 89, 2, '146253920', '219380880', NULL, 2),
(14, 90, 3, '219380880', '292507840', NULL, 2),
(15, 91, 4, '292507840', '365634800', NULL, 2),
(16, 92, 0, '0', '73126960', NULL, 2),
(17, 93, 1, '73126960', '146253920', NULL, 2),
(18, 94, 2, '146253920', '219380880', NULL, 2),
(19, 95, 3, '219380880', '292507840', NULL, 2),
(20, 96, 4, '292507840', '365634800', NULL, 2);

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
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
-- Dumping data for table `file`
--

INSERT INTO `file` (`file_id`, `request_id`, `joint_id`, `py_channel`, `server_path`, `size`, `md5_hash`, `sha1_hash`, `sha256_hash`, `progress`, `init_date`) VALUES
(351, 520, 'MNX0K1', '283697', 'C:/xampp/htdocs/JDS/storage/MNX0K1/520/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-04-18 22:44:14'),
(352, 521, '9BSW1Y', '543026', 'C:/xampp/htdocs/JDS/storage/9BSW1Y/521/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-04-19 00:36:19');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group`
--

DROP TABLE IF EXISTS `joint_group`;
CREATE TABLE `joint_group` (
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `py_channel` varchar(12) NOT NULL,
  `access_limit` int(2) NOT NULL DEFAULT 10,
  `expiry_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `date_created` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `joint_group`
--

INSERT INTO `joint_group` (`joint_id`, `user_id`, `py_channel`, `access_limit`, `expiry_date`, `date_created`) VALUES
('9BSW1Y', 2, '543026', 10, '2021-05-19 00:36:12', '2021-04-19 00:36:12'),
('MNX0K1', 2, '283697', 10, '2021-05-18 22:43:51', '2021-04-18 22:43:51');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group_member`
--

DROP TABLE IF EXISTS `joint_group_member`;
CREATE TABLE `joint_group_member` (
  `id` int(12) NOT NULL,
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `joint_role` varchar(20) NOT NULL DEFAULT 'member',
  `date_added` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `joint_group_member`
--

INSERT INTO `joint_group_member` (`id`, `joint_id`, `user_id`, `joint_role`, `date_added`) VALUES
(417, 'MNX0K1', 2, 'owner', '2021-04-18 22:43:51'),
(418, '9BSW1Y', 2, 'owner', '2021-04-19 00:36:12');

-- --------------------------------------------------------

--
-- Table structure for table `svr_download_request`
--

DROP TABLE IF EXISTS `svr_download_request`;
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
-- Dumping data for table `svr_download_request`
--

INSERT INTO `svr_download_request` (`request_id`, `joint_id`, `user_id`, `url`, `ext`, `size`, `bytes`, `max_chunk_size`, `init`, `request_datetime`) VALUES
(520, 'MNX0K1', 2, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', '365634800', 'auto', 4, '2021-04-18 22:43:51'),
(521, '9BSW1Y', 2, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', '365634800', 'auto', 4, '2021-04-19 00:36:12');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(12) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `hash` text NOT NULL,
  `joinedOn` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `password`, `hash`, `joinedOn`) VALUES
(1, 'admin', 'admin%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:21'),
(2, 'stephen', 'stevenoosunrinde%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:23'),
(3, 'myMacBook', 'mac%40mail.com', '$2y$10$8fh0wyl4mQ2yzG6qJPqFGePgr6xE26LDUIYwY9lVMyzFlvTzcFg5.', 'uk2ZxXt5ovOR', '2021-02-19 10:17:58');

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
  ADD KEY `chunk_id` (`chunk_id`);

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
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=286;

--
-- AUTO_INCREMENT for table `chunk`
--
ALTER TABLE `chunk`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT for table `chunk_child`
--
ALTER TABLE `chunk_child`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `file_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=353;

--
-- AUTO_INCREMENT for table `joint_group_member`
--
ALTER TABLE `joint_group_member`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=419;

--
-- AUTO_INCREMENT for table `svr_download_request`
--
ALTER TABLE `svr_download_request`
  MODIFY `request_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=522;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
  ADD CONSTRAINT `chunk_child_ibfk_1` FOREIGN KEY (`chunk_id`) REFERENCES `chunk` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

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
