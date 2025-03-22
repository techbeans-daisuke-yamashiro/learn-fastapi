import yaml,sys
sys.path.append("/app")

from models import Base

import yaml
from sqlmodel import Session, SQLModel, create_engine
from models import Table1
from . import 

# SQLite の例（必要に応じて変更）
engine = create_engine("sqlite:///database.db")

# YAML ファイルを読み込む
def load_yaml(filepath: str):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# シーディング処理
def seed_table1(data: list[dict]):
    with Session(engine) as session:
        for item in data:
            record = Table1(**item)
            session.add(record)
        session.commit()

# メイン処理
def main():
    SQLModel.metadata.create_all(engine)
    data = load_yaml("seed.yaml")
    
    if "table1" in data:
        seed_table1(data["table1"])

if __name__ == "__main__":
    main()
