from se_model.data import DataTransform


transform = DataTransform(data_path='/Volumes/Samsung_T5/iCloud Drive/PhD/[Research] [Summer 21] SE Language Models/data/jsonl/stackoverflow.com/',
                          out_dir='../data/processed/',
                          recurse_dirs=True)
transform.transform()
