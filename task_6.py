import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8888))
    print("Подключен к серверу")
    print("Команды: upload <файл> , download <файл> , exit")
    
    while True:
        cmd = input("> ")
        
        if cmd == 'exit':
            break
        
        parts = cmd.split()
        if len(parts) < 2:
            print("Нужно: upload <файл> или download <файл>")
            continue
        
        action = parts[0]
        name = parts[1]
        
        if action == 'upload':
            client.send(b'UPLOAD')
            client.send(name.encode())
            
            f = open(name, "rb")
            data = f.read()
            f.close()
            
            client.send(str(len(data)).encode())
            client.send(data)
            
            resp = client.recv(1024).decode()
            print(resp)
        
        elif action == 'download':
            client.send(b'DOWNLOAD')
            client.send(name.encode())
            
            resp = client.recv(1024).decode()
            
            if resp == 'NOT_FOUND':
                print("Файл не найден")
            else:
                size = int(resp)
                client.send(b'READY')
                
                data = b''
                while len(data) < size:
                    data = data + client.recv(4096)
                
                f = open("downloaded_" + name, "wb")
                f.write(data)
                f.close()
                print("Скачан:", name)
        
        else:
            print("Неизвестная команда")
    
    client.close()
    print("Отключено")

def main():
    start_client()

if __name__ == "__main__":
    main()