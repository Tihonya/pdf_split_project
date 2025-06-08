import yaml

def load_tasks(path="/home/toha/pdf_split_project/.continue/prompts/task.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    tasks = load_tasks()
    for i, t in enumerate(tasks.get("steps", []), 1):
        print(f"{i}. {t['title']} — {t.get('description','')}")
        
if __name__ == "__main__":
    main()