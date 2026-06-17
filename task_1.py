def to_int(bytes_data):
    result = 0
    for i in range(len(bytes_data)):
        result = result + (bytes_data[i] << (i * 8))
    return result

def main():
    file = open("data.bin", "rb")
    
    signature = file.read(4)
    
    if signature == b'DATA':
        version_bytes = file.read(2)
        version = to_int(version_bytes)
        
        count_bytes = file.read(4)
        num_records = to_int(count_bytes)
        
        temp_list = []
        active_flags = 0
        
        for i in range(num_records):
            record = file.read(15)
            
            if len(record) < 15:
                break
            
            timestamp_bytes = record[0:8]
            timestamp = to_int(timestamp_bytes)
            
            id_bytes = record[8:12]
            sensor_id = to_int(id_bytes)
            
            temp_bytes = record[12:14]
            temp_raw = to_int(temp_bytes)
            
            if temp_raw >= 32768:
                temp_raw = temp_raw - 65536
            
            temp_c = temp_raw / 100.0
            
            flag = record[14]
            
            temp_list.append(temp_c)
            
            if flag != 0:
                active_flags = active_flags + 1
        
        if len(temp_list) > 0:
            avg_temp = sum(temp_list) / len(temp_list)
            print("Средняя температура:", avg_temp)
            print("Активных флагов:", active_flags)
    
    file.close()

if __name__ == "__main__":
    main()