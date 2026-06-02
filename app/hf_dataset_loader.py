from datasets import load_dataset
import os

output_dir = "data/huggingface"
os.makedirs(output_dir, exist_ok=True)

dataset = load_dataset("aai510-group1/telco-customer-churn", split="train")

df = dataset.to_pandas()

output_path = os.path.join(output_dir, "telco_customer_churn.csv")

df.to_csv(output_path, index=False)

print(f"Hugging Face dataset saved to {output_path}")
print(df.head())
