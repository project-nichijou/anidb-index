
CREATE_TABLE_ANIME_NAME = (
	'CREATE TABLE IF NOT EXISTS `anidb_anime_name` ('
	'	`aid`		INT UNSIGNED NOT NULL,'
	'	`name`		VARCHAR(200) NOT NULL,'
	'	PRIMARY KEY ( `aid`, `name` )'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)

CREATE_TABLE_LOG = (
	'CREATE TABLE IF NOT EXISTS `log` ('
	'	`time`		VARCHAR(20) NOT NULL,'
	'	`content`	LONGTEXT'
	') ENGINE=InnoDB CHARSET=utf8mb4'
)
