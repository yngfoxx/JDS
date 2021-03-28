-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2021 at 09:01 AM
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
  `local_net_addr` varchar(16) DEFAULT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `authlogin`
--

INSERT INTO `authlogin` (`id`, `user_id`, `deviceKey`, `usr_channel`, `local_net_addr`, `dateCreated`) VALUES
(147, 3, '861fa0b40531486db307453b00d36442ccbc1b2b282559c7072f493092ca8881c3e12e65e1725aeb90a1515d2a506b1db676a6cd82af1a77f75554aa2e212e64', NULL, NULL, '2021-02-19 22:26:44'),
(198, 1, '58489340715a7f0b2241696846787c21cf0b77d4ee7f0eb46a4b9b18d89cbdd742d0abf78f3b1b5155b66cf4522b81f47375428c4bc230d6ce69430c2f0afb5d', NULL, NULL, '2021-03-27 04:45:29'),
(203, 2, '309ae00604cdcb023a28f301f0c194ea98d6b2597a312b4fe42c7808b42e050e02a963531cf8860a8e506f7b7cc9147f173b29292ac3e941738d410f93dbc64c', NULL, '169.254.233.112', '2021-03-27 23:21:54');

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
(322, 466, '8XJC6N', '184362', 'C:/xampp/htdocs/JDS/storage/8XJC6N/466/', '852.29 KB', 'd4f5d7654bda4c9842291069b0551f7b', '58504516d5a244fde44dff940b13f57d80c8f021', '9d4ea39ce99f480f252fdbeb616a69b9b11ea7bb29576abe8ec201c2afd159aa', 0, '2021-03-12 09:24:45'),
(323, 467, 'TDLIV3', '549670', 'C:/xampp/htdocs/JDS/storage/TDLIV3/467/', '6.43 MB', '0f883e6f5db348671c1e26a7dfd2e5f3', 'f6ce20bb436939d331e320418399265872615b15', 'e13e94c34bbdeb3e88d897639878ca12782e955080abff7d5d82efaeba56e584', 94.47984450065759, '2021-03-27 22:48:53'),
(324, 467, 'TDLIV3', '549670', 'C:/xampp/htdocs/JDS/storage/TDLIV3/467/', '6.43 MB', '0f883e6f5db348671c1e26a7dfd2e5f3', 'f6ce20bb436939d331e320418399265872615b15', 'e13e94c34bbdeb3e88d897639878ca12782e955080abff7d5d82efaeba56e584', 94.47984450065759, '2021-03-27 22:48:59'),
(325, 467, 'TDLIV3', '549670', 'C:/xampp/htdocs/JDS/storage/TDLIV3/467/', '6.43 MB', '0f883e6f5db348671c1e26a7dfd2e5f3', 'f6ce20bb436939d331e320418399265872615b15', 'e13e94c34bbdeb3e88d897639878ca12782e955080abff7d5d82efaeba56e584', 94.47984450065759, '2021-03-27 22:52:50'),
(326, 467, 'TDLIV3', '549670', 'C:/xampp/htdocs/JDS/storage/TDLIV3/467/', '6.43 MB', '0f883e6f5db348671c1e26a7dfd2e5f3', 'f6ce20bb436939d331e320418399265872615b15', 'e13e94c34bbdeb3e88d897639878ca12782e955080abff7d5d82efaeba56e584', 94.47984450065759, '2021-03-27 22:52:55'),
(327, 467, 'TDLIV3', '549670', 'C:/xampp/htdocs/JDS/storage/TDLIV3/467/', '6.43 MB', '0f883e6f5db348671c1e26a7dfd2e5f3', 'f6ce20bb436939d331e320418399265872615b15', 'e13e94c34bbdeb3e88d897639878ca12782e955080abff7d5d82efaeba56e584', 94.47984450065759, '2021-03-27 22:52:58');

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
('8XJC6N', 1, '184362', 10, '2021-04-03 17:01:34', '2021-03-04 18:01:34'),
('TDLIV3', 2, '549670', 10, '2021-04-26 21:48:04', '2021-03-27 22:48:04');

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
(380, '8XJC6N', 1, 'owner', '2021-03-04 18:01:34'),
(383, '8XJC6N', 2, 'member', '2021-03-12 08:34:22'),
(387, 'TDLIV3', 2, 'owner', '2021-03-27 22:48:04');

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
  `max_chunk_size` varchar(11) NOT NULL DEFAULT 'auto',
  `init` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0 = ''Waiting''\r\n1 = ''Initialized''\r\n2 = ''Downloaded''\r\n3 = ''Compressing''\r\n4 = ''Splitting''\r\n5 = ''Chunkified''',
  `request_datetime` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `svr_download_request`
--

INSERT INTO `svr_download_request` (`request_id`, `joint_id`, `user_id`, `url`, `ext`, `size`, `max_chunk_size`, `init`, `request_datetime`) VALUES
(456, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:01:34'),
(458, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:13:33'),
(460, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-04 18:56:43'),
(462, '8XJC6N', 2, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-12 08:34:45'),
(464, '8XJC6N', 1, 'https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe', 'exe', '348.70 MB', 'auto', 4, '2021-03-12 08:59:57'),
(466, '8XJC6N', 1, 'https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg', 'jpg', '852.29 KB', 'auto', 4, '2021-03-12 09:15:42'),
(467, 'TDLIV3', 2, 'https://cdnb.artstation.com/p/assets/images/images/024/538/827/original/pixel-jeff-clipa-s.gif', 'gif', '6.57 MB', '20', 4, '2021-03-27 22:48:04');

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
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=204;

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `file_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=328;

--
-- AUTO_INCREMENT for table `joint_group_member`
--
ALTER TABLE `joint_group_member`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=388;

--
-- AUTO_INCREMENT for table `svr_download_request`
--
ALTER TABLE `svr_download_request`
  MODIFY `request_id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=468;

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
