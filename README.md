# datadog-dump1090

[![Total alerts](https://img.shields.io/lgtm/alerts/g/sashacmc/datadog-dump1090.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sashacmc/datadog-dump1090/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/sashacmc/datadog-dump1090.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sashacmc/datadog-dump1090/context:python)

Datadog custom check to report dump1090 statistic


## Introduction

Dump 1090 is a Mode S decoder specifically designed for RTLSDR devices.
https://github.com/antirez/dump1090

<img src="https://user-images.githubusercontent.com/28735879/204161783-7ca7ac86-4654-49bb-b74b-a40e641df49d.png" width="300">

This custom check report all stat on minute basis in dump1090 namespace: 

 * local: statistics about messages received from a local SDR dongle. Not present in --net-only mode. Has subkeys:
   * modeac: number of Mode A / C messages decoded
   * modes: number of Mode S preambles received. This is *not* the number of valid messages!
   * bad: number of Mode S preambles that didn't result in a valid message
   * unknown_icao: number of Mode S preambles which looked like they might be valid but we didn't recognize the ICAO address and it was one of the message types where we can't be sure it's valid in this case.
 * remote: statistics about messages received from remote clients. Only present in --net or --net-only mode. Has subkeys:
   * modeac: number of Mode A / C messages received.
   * modes: number of Mode S messages received.
   * bad: number of Mode S messages that had bad CRC or were otherwise invalid.
   * unknown_icao: number of Mode S messages which looked like they might be valid but we didn't recognize the ICAO address and it was one of the message types where we can't be sure it's valid in this case.
 * cpu: statistics about CPU use. Has subkeys:
   * demod: milliseconds spent doing demodulation and decoding in response to data from a SDR dongle
   * reader: milliseconds spent reading sample data over USB from a SDR dongle
   * background: milliseconds spent doing network I/O, processing received network messages, and periodic tasks.
 * cpr: statistics about Compact Position Report message decoding. Has subkeys:
   * surface: total number of surface CPR messages received
   * airborne: total number of airborne CPR messages received
   * global_ok: global positions successfuly derived
   * global_bad: global positions that were rejected because they were inconsistent
   * global_range: global positions that were rejected because they exceeded the receiver max range
   * global_speed: global positions that were rejected because they failed the inter-position speed check
   * global_skipped: global position attempts skipped because we did not have the right data (e.g. even/odd messages crossed a zone boundary)
   * local_ok: local (relative) positions successfully found
   * local_aircraft_relative: local positions found relative to a previous aircraft position
   * local_receiver_relative: local positions found relative to the receiver position
   * local_skipped: local (relative) positions not used because we did not have the right data
   * local_range: local positions not used because they exceeded the receiver max range or fell into the ambiguous part of the receiver range
   * local_speed: local positions not used because they failed the inter-position speed check
   * filtered: number of CPR messages ignored because they matched one of the heuristics for faulty transponder output
 * tracks: statistics on aircraft tracks. Each track represents a unique aircraft and persists for up to 5 minutes after the last message
   from the aircraft is heard. If messages from the same aircraft are subsequently heard after the 5 minute period, this will be counted
   as a new track.
   * all: total tracks created
   * single_message: tracks consisting of only a single message. These are usually due to message decoding errors that produce a bad aircraft address.
 * http_requests: number of HTTP requests handled.
 * messages: total number of messages accepted by dump1090 from any source

## Instructions

* Copy the custom check and check config file to the Datadog agent install directory
```
cp dump1090.yaml /etc/datadog-agent/conf.d/
cp dump1090.py /etc/datadog-agent/checks.d/
```

* Restart the Datadog agent
