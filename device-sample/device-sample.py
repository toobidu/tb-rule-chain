import os
import json
import time
import random
import math
import requests  # Dùng requests thay vì subprocess
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH ---
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN")
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST")
THINGSBOARD_PORT = os.getenv("THINGSBOARD_PORT")
TELEMETRY_ENDPOINT = f"http://{THINGSBOARD_HOST}:{THINGSBOARD_PORT}/api/v1/{DEVICE_TOKEN}/telemetry"

# Cập nhật tọa độ tâm cho khớp với SERVER (Dựa trên request JSON mới nhất của bạn)
CENTER_LAT = 21.02850
CENTER_LON = 105.85420

# Bán kính config (km)
# Server: Radius 500m + Buffer 15% (75m) = Outer 575m
INNER_SAFE_RADIUS = 0.450  # 450m (Chắc chắn Inside)
OUTER_TRIGGER_RADIUS = 0.600  # 600m (Chắc chắn Outside)

# Biến toàn cục lưu vị trí hiện tại
current_lat = CENTER_LAT
current_lon = CENTER_LON


def send_telemetry_requests(data):
    try:
        response = requests.post(TELEMETRY_ENDPOINT, json=data, timeout=5)
        if response.status_code == 200:
            print("✅ Dữ liệu đã gửi thành công!")
            return True
        else:
            print(f"❌ Lỗi gửi (HTTP {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def get_random_point_in_circle(center_lat, center_lon, min_radius_km, max_radius_km):
    """Tạo một điểm ngẫu nhiên nằm trong vành khuyên"""
    theta = random.uniform(0, 2 * math.pi)
    # Lấy căn bậc 2 để phân bố đều diện tích
    r = math.sqrt(random.uniform(min_radius_km ** 2, max_radius_km ** 2))

    # Quy đổi khoảng cách km sang độ (xấp xỉ)
    delta_lat = (r / 111.0) * math.cos(theta)
    delta_lon = (r / (111.0 * math.cos(math.radians(center_lat)))) * math.sin(theta)

    return round(center_lat + delta_lat, 6), round(center_lon + delta_lon, 6)


def generate_sample_data():
    global current_lat, current_lon

    # Random tốc độ (km/h)
    speed = round(random.uniform(30, 60), 2)

    # Quyết định chế độ ngẫu nhiên: 60% Inside, 40% Outside
    is_inside_target = random.random() < 0.6

    current_dist = haversine_distance(current_lat, current_lon, CENTER_LAT, CENTER_LON)

    # LOGIC DI CHUYỂN:
    # 1. Nếu đang ở vùng này mà muốn giữ nguyên vùng -> Di chuyển nhỏ mô phỏng xe chạy
    # 2. Nếu muốn đổi vùng (Inside -> Outside) -> Bắt buộc phải "nhảy" (Teleport) vì 5s không chạy kịp

    should_teleport = False

    if is_inside_target:
        target_mode = "INSIDE"
        if current_dist > INNER_SAFE_RADIUS: should_teleport = True  # Đang ở ngoài, muốn vào trong
        min_r, max_r = 0.0, INNER_SAFE_RADIUS
    else:
        target_mode = "OUTSIDE"
        if current_dist < OUTER_TRIGGER_RADIUS: should_teleport = True  # Đang ở trong, muốn ra ngoài
        min_r, max_r = OUTER_TRIGGER_RADIUS, OUTER_TRIGGER_RADIUS + 0.5  # Ra xa tối đa thêm 500m

    if should_teleport:
        print(f"🔄 Chuyển vùng sang {target_mode} (Teleport để test trigger)...")
        current_lat, current_lon = get_random_point_in_circle(CENTER_LAT, CENTER_LON, min_r, max_r)
    else:
        # Di chuyển tự nhiên (mô phỏng xe chạy)
        # Tính quãng đường đi trong 5s
        dist_move_km = (speed / 3600) * 5

        # Thử tìm điểm mới
        for _ in range(10):
            temp_lat, temp_lon = get_random_point_in_circle(current_lat, current_lon, 0, dist_move_km)
            # Kiểm tra xem điểm mới có vi phạm vùng mong muốn không
            new_dist = haversine_distance(temp_lat, temp_lon, CENTER_LAT, CENTER_LON)

            # Nếu mode Inside: phải < Max Radius. Nếu mode Outside: phải > Min Radius
            if (is_inside_target and new_dist <= max_r) or (not is_inside_target and new_dist >= min_r):
                current_lat, current_lon = temp_lat, temp_lon
                break
        # Nếu không tìm được điểm lân cận thỏa mãn, giữ nguyên vị trí cũ (đỡ bị nhảy loạn xạ)

    final_dist_m = haversine_distance(current_lat, current_lon, CENTER_LAT, CENTER_LON) * 1000
    print(f"📍 Vị trí: {current_lat}, {current_lon} | Cách tâm: {final_dist_m:.2f}m | Mode: {target_mode}")

    return {
        "latitude": current_lat,
        "longitude": current_lon,
        "speed": speed
    }


if __name__ == "__main__":
    print(f"🚀 Bắt đầu gửi dữ liệu đến: {TELEMETRY_ENDPOINT}")
    print(f"🎯 Tâm Geofence: {CENTER_LAT}, {CENTER_LON}")

    try:
        while True:
            data = generate_sample_data()
            send_telemetry_requests(data)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng script.")