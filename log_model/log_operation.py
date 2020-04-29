# -*- coding:utf-8 -*-
__author__ = "leo"

import logging

from log_model.properties_utils import Properties


def set_log_config():
    pro = Properties("log.properties").get_properties()

    log_config = {
        "filename": pro["filename"],
        "level": pro["level"]
    }

    logging.basicConfig(**log_config)


if __name__ == '__main__':
    set_log_config()
    logging.info("info log")