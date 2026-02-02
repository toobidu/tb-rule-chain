/*This is a filter switch node in a ThingsBoard rule chain*/
if (metadata.reset && metadata.ss_geofenceStatus !== "none") {
    return ["Reset"];
}
return ["No Action"];