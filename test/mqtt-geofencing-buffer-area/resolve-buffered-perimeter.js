/*This is a script transformation node in a ThingsBoard rule chain*/
metadata.latitude = msg.latitude;
metadata.longitude = msg.longitude;
metadata.deviceSpeed = msg.speed;
var ts = parseInt(metadata.ts);  
var areaStr = metadata.ss_area;
var currentInnerPerimeter = null;
var currentOuterPerimeter = null;
var reset = false;

if (areaStr) {
    try {
        var area = JSON.parse(areaStr);  
        
        if (area && area.perimeter && area.start_time && area.end_time) {
            var start = parseInt(area.start_time);
            var end = parseInt(area.end_time);
            
            if (ts >= start && ts <= end) {
                var radius = area.perimeter.radius;
                var buffer = radius * 0.15;  // 15% buffer
                var innerRadius = Math.max(0, radius - buffer);  
                var outerRadius = radius + buffer;
                
                var innerObj = {
                    latitude: area.perimeter.latitude,
                    longitude: area.perimeter.longitude,
                    radiusUnit: area.perimeter.radiusUnit || "METER",
                    radius: innerRadius
                };
                
                var outerObj = {
                    latitude: area.perimeter.latitude,
                    longitude: area.perimeter.longitude,
                    radiusUnit: area.perimeter.radiusUnit || "METER",
                    radius: outerRadius
                };
                
                currentInnerPerimeter = JSON.stringify(innerObj);
                currentOuterPerimeter = JSON.stringify(outerObj);

                metadata.start_time = start;
                metadata.end_time = end;
            } else if (ts > end){
                reset = true;
            }
        }
    } catch (e) {
        currentInnerPerimeter = null;
        currentOuterPerimeter = null;
    }
}

metadata.innerPerimeter = currentInnerPerimeter;  
metadata.outerPerimeter = currentOuterPerimeter;  
metadata.reset=reset;
return {msg: msg, metadata: metadata, msgType: msgType};