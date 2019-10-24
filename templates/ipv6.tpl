protocol bgp |NAME| {
    local as |MYAS|;
    neighbor |NEIGHBOR_IP| as |NEIGHBOR_AS|;
    ipv6 {
        import |IMPORT_POLICY|;
        export |EXPORT_POLICY|;
    };
    graceful restart on;
}