from database.utils import get_model_by_tablename, get_tablenames
from models import setup_models
from argparse import ArgumentParser
from core.settings import Settings
from sqlmodel import Session, SQLModel, create_engine
import yaml,os,sys

script_dir=os.getcwd()




def get_engine(settings: Settings):
    return create_engine(url=settings.get_database_url(),echo=settings.db_echo)


def get_args() -> ArgumentParser:
    parser = ArgumentParser(description="YAMLデータを読み込んでデータベースをシーディングします")
    parser.add_argument('--dryrun', '-r',
                        help='読み込みテストのみを行い、実際の書き込みは実行しません。',
                        action='store_true')
    parser.add_argument('-f', '--file',
                        default=f"{script_dir}/seed.yaml",
                        help='シードするデータが記述されYAMLファイルを指定します。',
                        required=False)
    return parser.parse_args()


# YAML ファイルを読み込む
def load_yaml(filepath: str):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# シーディング処理


def seed_table(model: SQLModel, data: list[dict], engine):
    with Session(engine) as session:
        for item in data:
            record = model(**item)
            session.add(record)
        session.commit()

# メイン処理


def main():
    settings = Settings()
    args = get_args()
    engine = get_engine(settings=settings)
    setup_models(engine=engine)

    data = load_yaml(args.file)
    for table_name in get_tablenames():
        if args.dryrun == False:
            seed_table(model=get_model_by_tablename(table_name),
                       data=data[table_name],
                       engine=engine)


if __name__ == "__main__":
    main()
