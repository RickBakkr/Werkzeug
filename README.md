Werkzeug - BIRD configuration generation tool
================================================

Werkzeug aims to offer an easy way to automatically configure BGP peerings and filters accordingly. These configurations or prefix lists are generated based on a JSON file in conf/peering.json.
You can configure a session to either import/export all, a custom filter, or a filter based on a IRRdb prefix list (+ default filter template).

Usage:
------

    ./generate.py - Generates new sessions / filters for peers

Dependancies:
-------------

    bgpq3  - https://github.com/snar/bgpq3

Authors:
-------

    Copyright (c) 2019-present, Rick Bakker <mail@rickbakker.eu>
