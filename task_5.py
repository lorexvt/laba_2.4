import os

def to_xml(obj, tag="root", level=0):
    spaces = "  " * level
    if type(obj) == dict:
        res = spaces + "<" + tag + ">\n"
        for k, v in obj.items():
            if type(v) == list:
                for item in v:
                    res = res + to_xml(item, k, level + 1)
            else:
                res = res + to_xml(v, k, level + 1)
        res = res + spaces + "</" + tag + ">\n"
        return res
    else:
        return spaces + "<" + tag + ">" + str(obj) + "</" + tag + ">\n"

def from_xml(s):
    s = s.strip()
    i = 0
    
    if s[i] != '<':
        return None
    
    i = i + 1
    tag_start = i
    while i < len(s) and s[i] != '>':
        i = i + 1
    tag = s[tag_start:i]
    
    i = i + 1
    content_start = i
    depth = 1
    
    while i < len(s):
        if s[i:i+2] == '</':
            depth = depth - 1
            if depth == 0:
                break
            i = i + 2
        elif s[i] == '<':
            depth = depth + 1
            i = i + 1
        else:
            i = i + 1
    
    content = s[content_start:i].strip()
    
    while i < len(s) and s[i] != '>':
        i = i + 1
    i = i + 1
    
    if content and content[0] == '<':
        res = {}
        pos = 0
        while pos < len(content):
            while pos < len(content) and content[pos] in ' \n\t':
                pos = pos + 1
            if pos >= len(content):
                break
            if content[pos] == '<':
                child = from_xml(content[pos:])
                if child:
                    k = list(child.keys())[0]
                    v = child[k]
                    if k in res:
                        if type(res[k]) != list:
                            res[k] = [res[k]]
                        res[k].append(v)
                    else:
                        res[k] = v
                pos = pos + len(to_xml(child, k))
        return {tag: res}
    else:
        return {tag: content}

def validate_xml(s):
    if s.count('<') != s.count('>'):
        return False
    
    stack = []
    i = 0
    while i < len(s):
        if s[i] == '<':
            if i + 1 < len(s) and s[i+1] == '/':
                j = i + 2
                while j < len(s) and s[j] != '>':
                    j = j + 1
                close_tag = s[i+2:j]
                if len(stack) == 0 or stack[-1] != close_tag:
                    return False
                stack.pop()
                i = j + 1
            elif i + 1 < len(s) and s[i+1] != '?':
                j = i + 1
                while j < len(s) and s[j] != '>' and s[j] != ' ':
                    j = j + 1
                open_tag = s[i+1:j]
                stack.append(open_tag)
                while j < len(s) and s[j] != '>':
                    j = j + 1
                i = j + 1
            else:
                i = i + 1
        else:
            i = i + 1
    
    return len(stack) == 0

def test_all_xml_files(folder="resource"):
    print("ПРОВЕРКА\n")
    
    if not os.path.exists(folder):
        print(folder, "не найдена!")
        os.mkdir(folder)
        print("Положите файлы в папку", folder)
        return
    
    files = os.listdir(folder)
    xml_files = []
    for f in files:
        if f.endswith('.xml'):
            xml_files.append(f)
    
    if not xml_files:
        print("Нет файлов в папке", folder)
        return
    
    good = 0
    bad = 0
    
    for filename in xml_files:
        filepath = os.path.join(folder, filename)
        f = open(filepath, "r", encoding="utf-8")
        content = f.read()
        f.close()
        
        if validate_xml(content):
            print(filename, "- ВАЛИДЕН")
            good = good + 1
        else:
            print(filename, "- НЕ ВАЛИДЕН")
            bad = bad + 1
    
    print("\n" + "="*40)
    print("ИТОГО: хороших -", good, ", плохих -", bad)

def main():
    test_all_xml_files("resource")

if __name__ == "__main__":
    main()