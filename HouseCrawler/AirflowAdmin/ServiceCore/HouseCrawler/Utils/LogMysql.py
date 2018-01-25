#coding=utf-8

import logging
import time
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

logger = logging.getLogger(__name__)

def log_in_mysql(url,status):

    mysql_path = "mysql+pymysql://root:@192.168.6.8:3306/scrapy_data?charset=utf8"
    engine=create_engine(mysql_path,echo=False)
    metadata=MetaData(engine)
    conn=engine.connect()

    try:
        fang_bj_log = Table('fang_bj_log',metadata,autoload=True)
    except Exception as e:
        logger.debug("%(Exception)r : %(e)r",{'Exception':Exception,'e':e})
        if isinstance(e,sqlalchemy.exc.NoSuchTableError):
            logger.debug("Cannot find the table and create a new one.")
            fang_bj_log = Table('fang_bj_log',metadata,
                                        Column('id',Integer,primary_key=True,autoincrement=True),
                                        Column('create_time',VARCHAR(30),index=True,nullable=False),
                                        Column('url',TEXT,index=True,nullable=False),
                                        Column('status',VARCHAR(255),index=True,nullable=False),
                                        mysql_engine="InnoDB",mysql_charset="utf8")
            fang_bj_log.create()
            logger.debug("success.")

    try:
        i = fang_bj_log.insert()
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        cur_i = i.values(create_time=cur_time,
                    url=url,
                    status=status)
        conn.execute(cur_i)
    except Exception as e:
        logger.debug("%(Exception)r : %(e)r",{'Exception':Exception,'e':e})
