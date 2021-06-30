from se_model.data import DataTransform
import os


transformer = DataTransform(data_path=os.getcwd(),
                            out_dir='/tmp/', recurse_dirs=False)
transformer.transform()

with open('/tmp/data.jsonl.processed', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line)
