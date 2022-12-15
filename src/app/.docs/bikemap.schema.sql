CREATE TABLE `todos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `summary` varchar(255) DEFAULT NULL,
  `detail` varchar(255) DEFAULT NULL,
  `label` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `label` (`label`),
  KEY `created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
