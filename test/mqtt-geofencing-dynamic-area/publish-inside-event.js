/*This is a script transformation node in a ThingsBoard rule chain*/
var event = {
    deviceId: metadata.deviceId,
    deviceName: metadata.deviceName,
    status: "INSIDE",
    latitude: msg.latitude,
    longitude: msg.longitude,
    timestamp: new Date().getTime()
};

return {msg: event, metadata: metadata, msgType: "GEOFENCE_EVENT"};