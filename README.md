Werkzeug - BIRD configuration generation tool
================================================

Werkzeug aims to offer an easy way to automatically configure BGP peerings and filters accordingly. These configurations or prefix lists are generated based on a YAML file, either provided using the -c argument or by default in conf/peering.yaml.
You can configure a session to either import/export all, a custom filter, or a filter based on a IRRdb prefix list (+ default filter template).

# WARNING: !! DO NOT USE IN PRODUCTION !!

Usage:
------

    Usage: python3 generate.py -a 65000 [options]
    
Options:
------

    Options:
      -h, --help            Overview of options to provide the generator with
      -a MYAS, --as-number=MYAS
                            Your Autonomous Systen Number
      -c FILE, --config=FILE
                            Path to router specific peering configuration YAML file
      -o DIRECTORY, --output=DIRECTORY
                            Directory to write the output files to 
                            - MAKE SURE IT IS EXISTANT! We do not create the directory! 
      --dry-run             Does not write generated configs, just outputs to screen
      
The name:
------
Fairly rudimentary, Werkzeug is the German word for "Tool". While not the most creative, I somehow felt it really appropriate and surely will get the job done.

Dependancies:
-------------

    bgpq3  - https://github.com/snar/bgpq3
    pyyaml - https://github.com/yaml/pyyaml

Authors:
-------

Copyright (c) 2019-present, Rick Bakker <mail@rickbakker.eu>
