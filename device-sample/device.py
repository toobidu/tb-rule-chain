import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH ---
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN_2")
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST")
THINGSBOARD_PORT = os.getenv("THINGSBOARD_PORT")
TELEMETRY_ENDPOINT = f"http://{THINGSBOARD_HOST}:{THINGSBOARD_PORT}/api/v1/{DEVICE_TOKEN}/telemetry"

# Tọa độ tâm (Cầu Chương Dương)
CENTER_LAT = 21.02850
CENTER_LON = 105.85420

# Cấu hình bán kính để in Log kiểm tra
RADIUS = 500
BUFFER_PERCENT = 0.15
BUFFER_VAL = RADIUS * BUFFER_PERCENT  # 75m
INNER_LIMIT = RADIUS - BUFFER_VAL  # 425m
OUTER_LIMIT = RADIUS + BUFFER_VAL  # 575m


def send_telemetry(data):
    try:
        response = requests.post(TELEMETRY_ENDPOINT, json=data, timeout=5)
        return response.status_code == 200
    except:
        return False


def get_coordinate_at_distance(distance_meters):
    """Tính toạ độ mới cách tâm distance_meters (Di chuyển về hướng Bắc cho đơn giản)"""
    delta_lat = distance_meters / 111320.0
    return round(CENTER_LAT + delta_lat, 7), CENTER_LON


def analyze_zone(distance):
    """Hàm phân tích lý thuyết để bạn so sánh với Dashboard"""
    if distance <= INNER_LIMIT:
        return "✅ AN TOÀN (Deep Inside)"
    elif distance >= OUTER_LIMIT:
        return "❌ RA NGOÀI (Deep Outside)"
    else:
        return "⚠️ VÙNG ĐỆM (Buffer Zone - Giữ trạng thái cũ)"


def run_simulation():
    print(f"🎯 Tâm: {CENTER_LAT}, {CENTER_LON}")
    print(f"📏 Cấu hình: Radius={RADIUS}m | Buffer={BUFFER_VAL}m")
    print(f"🔹 Inner Limit (<= {INNER_LIMIT}m): Tính là INSIDE")
    print(f"🔸 Outer Limit (> {OUTER_LIMIT}m): Tính là OUTSIDE")
    print("---------------------------------------------------")

    # Kịch bản: Đi từ 400m ra 650m (Bước nhảy 10m) -> Rồi quay lại
    # Range tạo ra: 400, 410, ..., 650
    distances_out = list(range(400, 660, 10))
    # Range quay về: 640, 630, ..., 400
    distances_in = list(range(640, 390, -10))

    full_path = distances_out + distances_in

    # Chạy liên tục không dừng
    while True:
        for dist in full_path:
            lat, lon = get_coordinate_at_distance(dist)

            payload = {
                "latitude": lat,
                "longitude": lon,
                "speed": 30
            }

            # In log màu mè để dễ nhìn
            zone_info = analyze_zone(dist)
            print(f"Khoảng cách: {dist}m | {zone_info}")

            send_telemetry(payload)

            # Chờ 3 giây để bạn kịp nhìn Dashboard
            time.sleep(10)


if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\nDừng test.")
