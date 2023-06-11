import os
import shutil

def create_sample(directories):
    for directory in directories:
        sample_directory = directory + '_sample'
        # create sample directory if it doesn't exist
        if not os.path.exists(sample_directory):
            os.makedirs(sample_directory)

        files = os.listdir(directory)
        for i, filename in enumerate(files):
            if i >= 50:  # stop after copying 50 files
                break
            shutil.copy(os.path.join(directory, filename),
                        os.path.join(sample_directory, filename))

def main():
    directories = ['7-8_processed', '8-9_processed', '9-10_processed', '11-14_processed', '14-16_processed']
    full_dirs = map(lambda x: os.path.join('data', x), directories)
    create_sample(full_dirs)

if __name__ == '__main__':
    main()


