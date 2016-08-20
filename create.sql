CREATE DATABASE trump;
USE trump;

DROP TABLE IF EXISTS `tweets`;

CREATE TABLE `tweets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `twitter_id` varchar(120) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
