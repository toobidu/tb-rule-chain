var now = new Date().getTime();
var schedule = JSON.parse(metadata.ss_schedules || '[]');
var areas = JSON.parse(metadata.ss_areas || '{}');
var currentPerimeter = null;
var currentInnerPerimeter = null;
var currentOuterPerimeter = null;
var currentArea = null;
var reset = true;

for (var i = 0; i < schedule.length; i++) {
    var shift = schedule[i];
    var start = parseInt(shift.start_time);
    var end = parseInt(shift.end_time);

    if (now >= start && now <= end) {
        currentArea = shift.area;
        if (areas[currentArea]) {
            var area = areas[currentArea];

            // Tính buffer 
            var radius = area.radius;
            var buffer = radius * 0.15;
            var innerRadius = Math.max(0, radius - buffer);
            var outerRadius = radius + buffer;

            // Tạo perimeter chính 
            var perimeterObj = {
                latitude: area.latitude,
                longitude: area.longitude,
                radius: radius,
                radiusUnit: area.radiusUnit || "METER"
            };
            currentPerimeter = JSON.stringify(perimeterObj);

            // Tạo innerPerimeter
            var innerObj = {
                latitude: area.latitude,
                longitude: area.longitude,
                radius: innerRadius,
                radiusUnit: area.radiusUnit || "METER"
            };
            currentInnerPerimeter = JSON.stringify(innerObj);

            // Tạo outerPerimeter
            var outerObj = {
                latitude: area.latitude,
                longitude: area.longitude,
                radius: outerRadius,
                radiusUnit: area.radiusUnit || "METER"
            };
            currentOuterPerimeter = JSON.stringify(outerObj);

            metadata.start_time = start;
            metadata.end_time = end;
        }

        reset = false;
        break;
    }
}

if (reset) {
    currentPerimeter = null;
    currentInnerPerimeter = null;
    currentOuterPerimeter = null;
}

metadata.perimeter = currentPerimeter;
metadata.innerPerimeter = currentInnerPerimeter;
metadata.outerPerimeter = currentOuterPerimeter;
metadata.current_area = currentArea;
metadata.reset = reset;

return { msg: msg, metadata: metadata, msgType: msgType };