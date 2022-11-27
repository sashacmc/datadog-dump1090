#!/usr/bin/python3

import json
import urllib.request

from checks import AgentCheck


class SmartMon(AgentCheck):
    def __init__(self, name, init_config, instances):
        super().__init__(name, init_config, instances)
        self.__last_timestamp = 0

    def check(self, instance):
        url = instance.get("url")
        req = urllib.request.urlopen(url + "/data/receiver.json")
        version = json.loads(req.read())["version"]
        req = urllib.request.urlopen(url + "/data/stats.json")
        stats = json.loads(req.read())["last1min"]

        tags = [f"version:{version}"]

        timestamp = stats["end"]
        if self.__last_timestamp == timestamp:
            return
        self.__last_timestamp = timestamp

        def stats_walk(prefix, stats):
            for k, v in stats.items():
                name = prefix + "." + k
                if type(v) is dict:
                    stats_walk(name, v)
                elif type(v) is int:
                    self.count(name, v, tags=tags)

        stats_walk("dump1090", stats)
