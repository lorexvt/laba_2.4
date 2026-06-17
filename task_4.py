import os

def to_json(obj):
    if type(obj) == dict:
        items = []
        for k, v in obj.items():
            if type(v) == str:
                items.append('"' + k + '":"' + v + '"')
            elif type(v) == int or type(v) == float:
                items.append('"' + k + '":' + str(v))
            elif type(v) == bool:
                items.append('"' + k + '":' + ('true' if v else 'false'))
            elif v == None:
                items.append('"' + k + '":null')
            elif type(v) == list:
                items.append('"' + k + '":' + to_json(v))
            elif type(v) == dict:
                items.append('"' + k + '":' + to_json(v))
        return "{" + ",".join(items) + "}"
    
    elif type(obj) == list:
        items = []
        for i in obj:
            items.append(to_json(i))
        return "[" + ",".join(items) + "]"
    
    elif type(obj) == str:
        return '"' + obj + '"'
    elif type(obj) == bool:
        return 'true' if obj else 'false'
    elif obj == None:
        return 'null'
    else:
        return str(obj)

def from_json(s):
    s = s.strip()
    
    if s[0] == '"':
        return s[1:-1]
    
    if s[0] == '{':
        s = s[1:-1]
        result = {}
        if s:
            parts = []
            depth = 0
            cur = ""
            for ch in s:
                if ch == '{' or ch == '[':
                    depth = depth + 1
                elif ch == '}' or ch == ']':
                    depth = depth - 1
                elif ch == ',' and depth == 0:
                    parts.append(cur)
                    cur = ""
                    continue
                cur = cur + ch
            if cur:
                parts.append(cur)
            
            for p in parts:
                i = 0
                while p[i] != ':':
                    i = i + 1
                key = p[:i].strip('"')
                value = p[i+1:]
                result[key] = from_json(value)
        return result
    
    if s[0] == '[':
        s = s[1:-1]
        result = []
        if s:
            parts = []
            depth = 0
            cur = ""
            for ch in s:
                if ch == '{' or ch == '[':
                    depth = depth + 1
                elif ch == '}' or ch == ']':
                    depth = depth - 1
                elif ch == ',' and depth == 0:
                    parts.append(cur)
                    cur = ""
                    continue
                cur = cur + ch
            if cur:
                parts.append(cur)
            
            for p in parts:
                result.append(from_json(p))
        return result
    
    if s == 'true':
        return True
    if s == 'false':
        return False
    if s == 'null':
        return None
    
    if '.' in s:
        return float(s)
    return int(s)

def validate_json(s):
    try:
        from_json(s)
        return True
    except:
        return False

def test_all_json_files(folder="resource"):
    print("ПРОВЕРКА\n")
    
    if not os.path.exists(folder):
        print("Папка", folder, "не найдена")
        os.mkdir(folder)
        print("Положите файлы в папку", folder)
        return
    
    files = os.listdir(folder)
    json_files = []
    for f in files:
        if f.endswith('.json'):
            json_files.append(f)
    
    if not json_files:
        print("Нет файлов в папке", folder)
        return
    
    good = 0
    bad = 0
    
    for filename in json_files:
        filepath = os.path.join(folder, filename)
        f = open(filepath, "r", encoding="utf-8")
        content = f.read()
        f.close()
        
        if validate_json(content):
            print(filename, "- ВАЛИДЕН")
            good = good + 1
        else:
            print( filename, "- НЕ ВАЛИДЕН")
            bad = bad + 1
    
    print("ИТОГ: хороших -", good, ", плохих -", bad)

def main():
    test_all_json_files("resource")

if __name__ == "__main__":
    main()