from csv_source import load_clean_job_records


a = load_clean_job_records("./job_positions_sample_200.csv")

for chunk in a:
    print(chunk.job_id)

