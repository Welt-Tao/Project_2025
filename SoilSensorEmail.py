import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# 邮件配置 (替换为你的实际信息)
FROM_EMAIL = "1876489656@qq.com" # 发件邮箱
EMAIL_PASSWORD = "akksgflpkcvneegg" # 邮箱应用密码
TO_EMAIL = "welt799@163.com" # 收件邮箱

# 传感器配置
SENSOR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# 邮件发送记录
email_history = []
MAX_EMAILS_PER_DAY = 4 # 每天最多发送4封邮件
DAILY_EMAIL_COUNT = 0
LAST_RESET_DATE = datetime.now().date()

def send_email(subject, body):
    """发送邮件函数"""
    global DAILY_EMAIL_COUNT

# 检查是否达到每日邮件上限
    if DAILY_EMAIL_COUNT >= MAX_EMAILS_PER_DAY:
        print("已达到每日邮件发送上限")
        return False

    try:
# 创建邮件
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL

# 发送邮件 (QQ邮箱配置)
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
 
# 记录发送历史
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_history.append(f"{timestamp} - {subject}")
        DAILY_EMAIL_COUNT += 1

        print(f"邮件已发送: {subject}")
        return True

    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

def check_daily_reset():
    """检查是否需要重置每日计数器"""
    global DAILY_EMAIL_COUNT, LAST_RESET_DATE

    today = datetime.now().date()
    if today != LAST_RESET_DATE:
        DAILY_EMAIL_COUNT = 0
        LAST_RESET_DATE = today
        print("已重置每日邮件计数器")

def read_sensor():
    """读取土壤湿度传感器状态"""
    return GPIO.input(SENSOR_PIN)

def main():
    try:
        print("土壤湿度监测系统启动...")
        print(f"发件邮箱: {FROM_EMAIL}")
        print(f"收件邮箱: {TO_EMAIL}")

# 初始测试邮件
        send_email("系统启动通知", "土壤湿度监测系统已成功启动")

        while True:
# 检查是否需要重置每日计数器
            check_daily_reset()

# 读取传感器状态
            sensor_state = read_sensor()

# 确定植物状态
            if sensor_state == GPIO.HIGH:
                status = "土壤干燥 - 需要浇水!"
                subject = " 请给植物浇水!"
            else:
                status = "土壤湿润 - 无需浇水"
                subject = "✅ 植物水分充足"

# 创建邮件内容
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = (
                f"植物状态报告\n\n"
                f"时间: {timestamp}\n"
                f"状态: {status}\n\n"
                f"今日已发送邮件数: {DAILY_EMAIL_COUNT}/{MAX_EMAILS_PER_DAY}"
            )

# 发送状态邮件
            send_email(subject, body)

# 显示当前状态
            print(f"[{timestamp}] {status}")

# 等待4小时 (4 * 60 * 60 秒)
            time.sleep(4 * 60 * 60)

    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
# 保存邮件历史记录
        with open("email_history.txt", "w") as f:
            f.write("邮件发送历史记录:\n")
            f.write("\n".join(email_history))
        print("邮件历史已保存到 email_history.txt")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
