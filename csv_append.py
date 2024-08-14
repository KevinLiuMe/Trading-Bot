import os
import csv

def append_line_to_csv(source_name, target_name, line_number):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    source_file = os.path.join(desktop_path, source_name)
    target_file = os.path.join(desktop_path, target_name)

    try:
        with open(source_file, 'r') as src, open(target_file, 'a', newline='') as tgt:
            reader = csv.reader(src)
            writer = csv.writer(tgt)

            # Skip lines until we reach the desired one
            for current_line, row in enumerate(reader, start=1):
                if current_line == line_number:
                    writer.writerow(row)
                    print(f"Appended line {line_number} from {source_name} to {target_name}")
                    return
            
            print(f"Line {line_number} does not exist in {source_name}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    source_name = input("Enter the name of the source CSV file: ")
    target_name = input("Enter the name of the target CSV file: ")
    line_number = int(input("Enter the line number to append: "))
    
    append_line_to_csv(source_name, target_name, line_number)
