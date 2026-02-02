/*
*This is a script transformation node in a ThingsBoard rule chain.
*/
var now = new Date().getTime();

var scheduleStr = metadata.ss_schedules || '[]';
var zonesStr = metadata.ss_zones || '{}';

var schedule = JSON.parse(scheduleStr);
var zones = JSON.parse(zonesStr);

var currentPerimeter = null;
var currentZone = null;

for (var i = 0; i < schedule.length; i++) {
    var shift = schedule[i];
    var start = parseInt(shift.start_time);
    var end = parseInt(shift.end_time);

    if (now >= start && now <= end) {
        currentZone = shift.zone;
        if (zones[currentZone]) {
            var zone = zones[currentZone];

            var perimeterObj = {
                latitude: zone.latitude,
                longitude: zone.longitude,
                radius: zone.radius,
                radiusUnit: zone.radiusUnit || "METER"
            };

            currentPerimeter = JSON.stringify(perimeterObj);
        }
        break;
    }
}

if (currentPerimeter) {
    metadata.perimeter = currentPerimeter;
    metadata.current_zone = currentZone;
} else {
    metadata.perimeter = null;
}

return { msg: msg, metadata: metadata, msgType: msgType };