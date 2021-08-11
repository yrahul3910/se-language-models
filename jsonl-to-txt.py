from se_model.data import DataTransform


transform = DataTransform(data_path='/Users/ryedida/Library/Mobile Documents/com~apple~CloudDocs/PhD/[Research] [Summer 21] SE Language Models/data/jsonl/',
                          out_dir='../data/processed/',
                          recurse_dirs=True)
transform.transform()
