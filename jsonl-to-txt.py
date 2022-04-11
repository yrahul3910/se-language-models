from se_model.data import DataTransform


transform = DataTransform(data_path='./stackoverflow.com/',
                          out_dir='./data/processed/',
                          recurse_dirs=True)
transform.transform()
