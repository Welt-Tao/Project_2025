# send_email.py (参考版本，不需要实际创建)
import smtplib
from email.message import EmailMessage

# 配置邮箱信息 (实际使用时会替换)
FROM_EMAIL = "1876489656@qq.com"
EMAIL_PASSWORD = "akksgflpkcvneegg"
TO_EMAIL = "welt799@163.com"

def send_email(subject, body):
    """发送邮件函数"""
    try:
# 创建邮件
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL

# QQ邮箱配置 (使用SSL)
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

# 测试代码
if __name__ == "__main__":
    send_email("测试邮件", "这是一封来自树莓派的测试邮件")
