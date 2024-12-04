#!/bin/bash
/usr/local/bin/confd -onetime -backend env -confdir /etc/confd
/opt/start-jmx-scraper.sh