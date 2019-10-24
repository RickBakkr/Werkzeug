protocol bgp |NAME| {
    local as |MYAS|;
    neighbor |NEIGHBOR_IP| as |NEIGHBOR_AS|;
    ipv4 {
        import |IMPORT_POLICY|;
        export |EXPORT_POLICY|;
    };
    graceful restart on;
    |MD5_PASSWORD|
    |IMPORT_LIMIT|
}