from datetime import datetime, timezone, timedelta

def calculate_time_range():
    print("--- Tính toán StartTime và EndTime (UTC+7) ---")

    try:
        # 1. Nhập Start Time
        print(">> Nhập thời gian bắt đầu (Start Time):")
        day = int(input("   Ngày (DD): "))
        month = int(input("   Tháng (MM): "))
        year = int(input("   Năm (YYYY): "))
        hour = int(input("   Giờ (0-23): "))
        minute = int(input("   Phút (0-59): "))

        # 2. Nhập khoảng thời gian (Minutes Next)
        print("\n>> Nhập thời lượng:")
        minutes_next = int(input("   Số phút cộng thêm (Minutes Next): "))

        # 3. Xử lý logic thời gian
        # Định nghĩa múi giờ UTC+7
        tz_vietnam = timezone(timedelta(hours=7))

        # Tạo đối tượng startTime
        start_dt = datetime(year, month, day, hour, minute, tzinfo=tz_vietnam)

        # Tính toán endTime bằng cách cộng thêm số phút vào startTime
        end_dt = start_dt + timedelta(minutes=minutes_next)

        # 4. Chuyển đổi sang Milliseconds
        start_ms = int(start_dt.timestamp() * 1000)
        end_ms = int(end_dt.timestamp() * 1000)

        # 5. Xuất kết quả
        print("-" * 40)
        print(f"Start Time ({start_dt.strftime('%d/%m/%Y %H:%M')}): {start_ms}")
        print(f"End Time   ({end_dt.strftime('%d/%m/%Y %H:%M')}): {end_ms}")
        print("-" * 40)
        print(f"Chênh lệch: {minutes_next} phút")

    except ValueError:
        print("Lỗi: Dữ liệu nhập vào không phải là số hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    calculate_time_range()