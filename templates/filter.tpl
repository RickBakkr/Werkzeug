filter |NAME|
prefix set |LIST_NAME|; {

|LIST_DEFINITION|

    reject_bogon_asns();
    reject_bogon_prefixes();
    reject_long_aspaths();
    #reject_transit_paths(); # maybe activate some day
    reject_default_route();

    if net ~ |LIST_NAME| then accept;

    reject;
}