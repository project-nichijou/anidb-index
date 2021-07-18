**REFACTORING IN PROGRESS, DO NOT USE**

**正在重构，请勿使用**

# 0x01 AniDB Index [Project Nichijou]

本项目作为项目[Project Nichijou](https://github.com/project-nichijou)中的子项目，是[AniDB](anidb.net)的数据库标题索引，用于构建番剧数据库。完整内容详见: https://github.com/project-nichijou/intro

## 思路与流程

本repo只包含：
- 从[官方API](https://wiki.anidb.net/API)获取标题`XML`数据
- 写入数据库

## 环境

- MySQL 5.7.4 +
- Python 3.6 +
- mysql-connector-python
- click

## 配置方法

本项目有一个配置文件：
- `database/database_settings.py`

可以发现这此文件在本`repo`中只有`_template`，需要将这两个`template`配置好并复制、重命名。

关于配置字段的具体含义，文件中都有注释，可以自行查阅。

## 使用方法

通过CLI调用，下面是说明：

```
$ python3 main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dellog    delete loggings in the database.
  download  download the anidb title index database dump
  parse     download then save the parse and save the result into the...
```

```
$ python3 main.py download --help
Usage: main.py download [OPTIONS]

  download the anidb title index database dump

Options:
  --url TEXT      use other url to download database instead of the one in the
                  configuration file
  --ignore_cache  whether to ignore cache files
  --help          Show this message and exit.
```

```
$ python3 main.py dellog --help
Usage: main.py dellog [OPTIONS]

  delete loggings in the database.

Options:
  --before TEXT  delete the loggings which are before the time in the
                 database. default is None, which means delete all. data
                 format: YYYY-MM-DD hh:mm:ss
  --help         Show this message and exit.
```

## 关于数据库

本项目目前使用MySQL作为数据库，更多的数据库日后~~可能~~会进行支持，如果有兴趣可以提交PR，持续关注。

此外，当前的默认数据库名称为`anidb`，本工具会自动新建数据库以及数据表 (若不存在) 。如果和本地数据库名称有冲突，可以在`database/database_settings.py`中修改。

下面为各张`table`的定义语句:

```sql
CREATE TABLE IF NOT EXISTS `anidb_anime_name` (
	`aid`		INT UNSIGNED NOT NULL,
	`name`		VARCHAR(200) NOT NULL,
	PRIMARY KEY ( `aid`, `name` )
) ENGINE=InnoDB CHARSET=utf8mb4
```

```sql
CREATE TABLE IF NOT EXISTS `log` (
	`time`		VARCHAR(20) NOT NULL,
	`content`	LONGTEXT
) ENGINE=InnoDB CHARSET=utf8mb4
```

## 关于`json_generator.py`

其用于初始化`nichijou`私有数据库，谨慎使用。
