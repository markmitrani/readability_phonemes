import os

def remove_last_line_Weekly(directory, output_directory):
    # iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    lines = file.readlines()

                if len(lines) > 0 and "Weekly Reader Corporation" in lines[-1]:
                    # remove last line
                    lines = lines[:-1]

                    # create output directory if it doesn't exist
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                    with open(os.path.join(output_directory, filename), 'w') as file:
                        file.writelines(lines)
                else:
                    print("Couldn't perform operation on file: "+filename)
            except:
                print("MANUALLY HANDLE "+filename)


def remove_last_line_BiteSize(directory, output_directory):
    # iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(directory, filename), 'r') as file:
                    lines = file.readlines()

                if len(lines) > 0 and "browser software or enabling style sheets (CSS)" in lines[-1]:
                    # remove last line
                    lines = lines[:-1]
                    if len(lines) > 0 and "BBC is not responsible for the content" in lines[-1]:
                        lines = lines[:-1]
                    else:
                        print(filename + " had CSS line but not BCC content line")

                    # create output directory if it doesn't exist
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                    with open(os.path.join(output_directory, filename), 'w') as file:
                        file.writelines(lines)
                else:
                    print("Couldn't perform operation on file: "+filename+"in "+directory)
            except:
                print("MANUALLY HANDLE "+filename)

def execute_Weekly_process():
    directories = ['7-8', '8-9', '9-10']
    for directory in directories:
        directory_path = os.path.join('data', directory)
        output_directory = directory_path + '_processed'
        remove_last_line_Weekly(directory_path, output_directory)

def execute_BiteSize_process():
    directories = ['11-14', '14-16']
    for directory in directories:
        directory_path = os.path.join('data', directory)
        output_directory = directory_path + '_processed'
        remove_last_line_BiteSize(directory_path, output_directory)

def main():
    execute_BiteSize_process()

if __name__ == '__main__':
    main()