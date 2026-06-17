def main():
    divisor = 73 * 73 + 29
    
    f_in = open("numbers.txt", "r")
    f_out = open("result.txt", "w")
    
    for line in f_in:
        numbers = line.split()
        for num_str in numbers:
            num = int(num_str)
            if num % 7 == 0:
                result = num * 100 / divisor
                f_out.write(str(result) + "\n")
                print(num, "->", result)
    
    f_in.close()
    f_out.close()
    print("Результат сохранен в result.txt")

if __name__ == "__main__":
    main()