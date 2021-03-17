-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2021 at 11:56 AM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

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
CREATE TABLE IF NOT EXISTS `applications` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `app_ID` text NOT NULL,
  `app_name` text NOT NULL,
  `app_desc` text NOT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
CREATE TABLE IF NOT EXISTS `authlogin` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `user_id` int(12) NOT NULL,
  `deviceKey` text NOT NULL,
  `usr_channel` text DEFAULT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `authlogin`
--

INSERT INTO `authlogin` (`id`, `user_id`, `deviceKey`, `usr_channel`, `dateCreated`) VALUES
(147, 3, '861fa0b40531486db307453b00d36442ccbc1b2b282559c7072f493092ca8881c3e12e65e1725aeb90a1515d2a506b1db676a6cd82af1a77f75554aa2e212e64', NULL, '2021-02-19 22:26:44'),
(155, 2, '915fdefb180e1dbc98348f347df329558833788e95d922ee262bfcd1ba97d3f5231d5016924fe261fc6c8d53b58aeef017352416e3d4fe1292af203130bdc81b', NULL, '2021-03-12 08:34:09'),
(156, 1, '809d4c16604ed1ead9aafdefec9bace1a6aea063708375c08dc1c1a8bba8160ed9a885dfa65d2953dd664b896265e565f7de7ac1f3865fcd85a7d9644c598bbb', NULL, '2021-03-16 07:35:21');

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
CREATE TABLE IF NOT EXISTS `file` (
  `file_id` int(12) NOT NULL AUTO_INCREMENT,
  `request_id` int(12) NOT NULL,
  `joint_id` varchar(12) NOT NULL,
  `py_channel` text NOT NULL,
  `server_path` text DEFAULT NULL,
  `size` text DEFAULT NULL,
  `md5_hash` text NOT NULL,
  `sha1_hash` text NOT NULL,
  `sha256_hash` text NOT NULL,
  `progress` double DEFAULT 0,
  `init_date` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`file_id`),
  KEY `file_ibfk_1` (`joint_id`),
  KEY `file_ibfk_2` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=323 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `file`
--

INSERT INTO `file` (`file_id`, `request_id`, `joint_id`, `py_channel`, `server_path`, `size`, `md5_hash`, `sha1_hash`, `sha256_hash`, `progress`, `init_date`) VALUES
(307, 456, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/456/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-04 18:01:39'),
(308, 458, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/458/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-04 18:14:00'),
(309, 460, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/460/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-04 18:56:47'),
(310, 460, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/460/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-04 19:25:27'),
(311, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:02'),
(312, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:05'),
(313, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:07'),
(314, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:10'),
(315, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:12'),
(316, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:13'),
(317, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:14'),
(318, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:17'),
(319, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:56:19'),
(320, 462, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/462/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 08:57:01'),
(321, 464, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/464/', '348.70 MB', 'fc5f402f65fe8491403d7c9939953e6a', '2ff79bbeb6cd35c8c2d3a3305db9993f6fef8c42', 'd5d18c36ef709a28cb92bcf13def99254a3e4cb10b0c90bcc024dfc920be8285', 100, '2021-03-12 09:00:00'),
(322, 466, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/466/', '852.29 KB', 'd4f5d7654bda4c9842291069b0551f7b', '58504516d5a244fde44dff940b13f57d80c8f021', '9d4ea39ce99f480f252fdbeb616a69b9b11ea7bb29576abe8ec201c2afd159aa', 0, '2021-03-12 09:24:45');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group`
--

DROP TABLE IF EXISTS `joint_group`;
CREATE TABLE IF NOT EXISTS `joint_group` (
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `py_channel` varchar(12) NOT NULL,
  `access_limit` int(2) NOT NULL DEFAULT 10,
  `expiry_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`joint_id`),
  KEY `joint_group_ibfk_1` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `joint_group`
--

INSERT INTO `joint_group` (`joint_id`, `user_id`, `py_channel`, `access_limit`, `expiry_date`, `date_created`) VALUES
('8XJC6N', 1, '184362', 10, '2021-04-03 17:01:34', '2021-03-04 18:01:34');

-- --------------------------------------------------------

--
-- Table structure for table `joint_group_member`
--

DROP TABLE IF EXISTS `joint_group_member`;
CREATE TABLE IF NOT EXISTS `joint_group_member` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `joint_role` varchar(20) NOT NULL DEFAULT 'member',
  `date_added` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `joint_group_member_ibfk_1` (`joint_id`),
  KEY `joint_group_member_ibfk_2` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=387 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `joint_group_member`
--

INSERT INTO `joint_group_member` (`id`, `joint_id`, `user_id`, `joint_role`, `date_added`) VALUES
(380, '8XJC6N', 1, 'owner', '2021-03-04 18:01:34'),
(383, '8XJC6N', 2, 'member', '2021-03-12 08:34:22');

-- --------------------------------------------------------

--
-- Table structure for table `svr_download_request`
--

DROP TABLE IF EXISTS `svr_download_request`;
CREATE TABLE IF NOT EXISTS `svr_download_request` (
  `request_id` int(12) NOT NULL AUTO_INCREMENT,
  `joint_id` varchar(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `url` text NOT NULL,
  `ext` varchar(5) NOT NULL,
  `size` text NOT NULL,
  `max_chunk_size` varchar(11) NOT NULL DEFAULT 'auto',
  `init` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0 = ''Waiting''\r\n1 = ''Initialized''\r\n2 = ''Downloaded''\r\n3 = ''Compressing''\r\n4 = ''Splitting''\r\n5 = ''Chunkified''',
  `request_datetime` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`request_id`),
  KEY `svr_download_request_ibfk_1` (`joint_id`),
  KEY `svr_download_request_ibfk_2` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=467 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `svr_download_request`
--

INSERT INTO `svr_download_request` (`request_id`, `joint_id`, `user_id`, `url`, `ext`, `size`, `max_chunk_size`, `init`, `request_datetime`) VALUES
(456, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:01:34'),
(458, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:13:33'),
(460, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:56:43'),
(462, '8XJC6N', 2, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-12 08:34:45'),
(464, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-12 08:59:57'),
(466, '8XJC6N', 1, 'https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg', 'jpg', '852.29 KB', 'auto', 4, '2021-03-12 09:15:42');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(12) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `hash` text NOT NULL,
  `joinedOn` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `password`, `hash`, `joinedOn`) VALUES
(1, 'admin', 'admin%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:21'),
(2, 'stephen', 'stevenoosunrinde%40mail.com', '$2y$10$KKqc7DZ9KxFQtiJcCQTSl.YAikxE7sHWQ8vAmc3G5maHnxxL751cG', 'TOmyrQ8aWcpb', '2020-12-20 05:37:23'),
(3, 'myMacBook', 'mac%40mail.com', '$2y$10$8fh0wyl4mQ2yzG6qJPqFGePgr6xE26LDUIYwY9lVMyzFlvTzcFg5.', 'uk2ZxXt5ovOR', '2021-02-19 10:17:58');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authlogin`
--
ALTER TABLE `authlogin`
  ADD CONSTRAINT `authlogin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

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
