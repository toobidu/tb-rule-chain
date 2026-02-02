/*
Test rule chain for MQTT telemetry routing.
Routes telemetry to:
- device/{entityId}/{deviceName}/telemetry if assigned
- device/none/{deviceName}/telemetry if unassigned
Uses dynamic topic pattern variable due to MQTT wildcard publish limitation.
*/

/*
FLow: get key name "entityId" from server attributes by Originator attributes node to script transformation node
*/

/*
INPUT: metadata.deviceName, metadata.ss_entityId
OUTPUT: topic pattern: ${topic}
*/

/* Script transformation node */
var msg = msg;  
var metadata = metadata;  
var msgType = msgType;  
var deviceName = metadata.deviceName; 
var entityId = metadata.ss_entityId;
if (!entityId || entityId === 'none' || entityId === null) {
    metadata.topic = 'device/none/' + deviceName + '/telemetry';
} else {
    metadata.topic = 'device/' + entityId + '/' + deviceName + '/telemetry';
}
return {msg: msg, metadata: metadata, msgType: msgType};