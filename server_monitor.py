import psutil
import datetime
import csv
import os

# 로그를 저장할 파일명
LOG_FILE = "server_health_log.csv"

def check_server_health():
    # 현재 시간 측정
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 서버 자원 사용량 추출
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # 임계치 설정 (CPU 80% 이상이거나 디스크 90% 이상이면 WARNING)
    status = "NORMAL"
    if cpu_usage > 80.0 or disk.percent > 90.0:
        status = "WARNING"

    # 엑셀(CSV)에 기록할 데이터 형태
    log_data = [now, cpu_usage, memory.percent, disk.percent, status]

    # 파일이 없으면 헤더(첫 줄)를 만들고, 있으면 내용만 추가(a 모드)
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "CPU Usage(%)", "Memory Usage(%)", "Disk Usage(%)", "Status"])
        writer.writerow(log_data)

    print(f"[{now}] 상태: {status} | CPU: {cpu_usage}% | 메모리: {memory.percent}% | 디스크: {disk.percent}%")

if __name__ == "__main__":
    check_server_health()
