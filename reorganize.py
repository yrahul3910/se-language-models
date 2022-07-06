from pathlib import Path
import sys
import random
from tqdm import tqdm


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: reorganize.py IN_PATH OUT_PATH')
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.exists():
        print('Path does not exist.')
        sys.exit(2)

    out_path = Path(sys.argv[2])
    if not out_path.exists():
        out_path.mkdir()

    train_ratio = 0.85
    val_ratio = 0.1
    test_ratio = 0.05

    train_path = out_path / 'train'
    if not train_path.exists():
        train_path.mkdir()

    # Set up train/test/val files
    (out_path / 'train.txt').touch()
    (out_path / 'valid.txt').touch()
    (out_path / 'test.txt').touch()

    train_file = open(out_path / 'train.txt', 'w')
    valid_file = open(out_path / 'valid.txt', 'w')
    test_file = open(out_path / 'test.txt', 'w')

    for file in tqdm(list(in_path.rglob('*.processed'))):
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [x for x in lines if len(x)]

            for line in lines:
                rand = random.random()
                if rand <= train_ratio:
                    train_file.writelines([line])
                elif rand <= train_ratio + val_ratio:
                    valid_file.writelines([line])
                else:
                    test_file.writelines([line])

    train_file.close()
    valid_file.close()
    test_file.close()
