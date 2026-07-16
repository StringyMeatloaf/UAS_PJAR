-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 14, 2026 at 04:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mediashare`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `verification_token` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_verified`, `verification_token`, `created_at`) VALUES
(7, 'rayakha', 'damanikrayakha@gmail.com', 'scrypt:32768:8:1$Dt4PN1L13V37V2Aj$8b9b6281a15db26b51aedacdd58cc22b584eb53362250d8594216b7940dcd818d6f8abb7c34fa2ff5c4f5775438d7ccf5a55201f5febaa478f488adfc5f813f2', 1, NULL, '2026-07-12 00:26:45'),
(11, 'raya', 'sweeprmonk@gmail.com', 'scrypt:32768:8:1$MAhjYQNKmgoFoTy6$b8be30162a81c699d3d4cb84c5c455560ef53fa062b145ad73aa74252952e505e0c11602fe71137660edd338ea04ce2f0400a9fc86128a9b00b21a4f2667ea14', 0, 'COpY2KvUBGG5m9aZgDa_oBnMuUVQx_JCdfMv2Ouh-lI', '2026-07-12 03:54:28'),
(12, 'ray', 'stringymeatlover@gmail.com', 'scrypt:32768:8:1$71aTvuYR1PRq7MKY$af501bbbc8076bb82355fd56701dbe4fb46df4cbef2ad8f3624cc28e6ffc3b43daf62e387306d4a4f5ff8215b29d5c87b377f707632d34bab32a53403441f401', 1, NULL, '2026-07-12 07:56:50');

-- --------------------------------------------------------

--
-- Table structure for table `videos`
--

CREATE TABLE `videos` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `filepath` varchar(255) NOT NULL,
  `filesize` bigint(20) NOT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `videos`
--

INSERT INTO `videos` (`id`, `user_id`, `filename`, `filepath`, `filesize`, `uploaded_at`) VALUES
(1, 7, 'sample.mp4', 'sample.mp4', 579635, '2026-07-12 06:43:00'),
(2, 7, '2026-05-21 22-00-07.mkv', '2026-05-21 22-00-07.mkv', 25815669, '2026-07-12 06:43:44'),
(3, 7, '2024-11-30 03-18-46.mp4', '2024-11-30 03-18-46.mp4', 561025, '2026-07-12 07:37:40'),
(4, 7, 'IMK_Video Penjelasan.mp4', 'IMK_Video Penjelasan.mp4', 68026603, '2026-07-12 09:58:40');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
