import json
import random
import string


def generate_random_string(length):
    # 무작위 문자열 생성
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_email(name):
    # 무작위 이메일 생성
    domains = ["example.com", "test.com", "sample.com", "email.com"]
    return f"{name}@{random.choice(domains)}"

def generate_random_password(length):
    # 무작위 비밀번호 생성
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

if __name__ == "__main__":
    data = []
    record_count = 200
    for i in range(1, record_count+1):
        name = "홍길동" + str(i)
        obj = {
            "name": name,
            "email": generate_random_email(name.lower()),
            "password": generate_random_password(10),
            "manager": random.choice(["on", "off"]),
            "sellist1": random.choice(["Option1", "Option2", "Option3"]),
            "text": f"안녕하세요. {name}입니다."
        }
        data.append(obj)

    # JSON 형식으로 변환
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    # JSON 파일로 저장
    with open('./models/users_data.json', 'w', encoding='utf-8') as file:
        file.write(json_data)    
