import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, app
from app.db_models import HostStar, Planet

import argparse

DEFAULT_CSV = os.path.join(os.path.dirname(__file__), 'PSCompPars_2025.05.08_13.14.37.csv')

def import_csv(csv_path=DEFAULT_CSV):
    with app.app_context():
        db.create_all()  # 自动建表
        success_count = 0
        fail_count = 0
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            host_star_cache = {}
            for idx, row in enumerate(reader, 1):
                try:
                    hostname = row['hostname'].strip()
                    # 先查找或创建 HostStar
                    if hostname in host_star_cache:
                        host_star = host_star_cache[hostname]
                    else:
                        host_star = HostStar.query.filter_by(hostname=hostname).first()
                        if not host_star:
                            host_star = HostStar(
                                hostname=hostname,
                                sy_pnum=int(row['sy_pnum']) if row['sy_pnum'] else None,
                                sy_dist=float(row['sy_dist']) if row['sy_dist'] else None,
                                sy_disterr1=float(row['sy_disterr1']) if row['sy_disterr1'] else None,
                                sy_disterr2=float(row['sy_disterr2']) if row['sy_disterr2'] else None,
                            )
                            db.session.add(host_star)
                            db.session.flush()  # 获取 id
                        host_star_cache[hostname] = host_star
                    # 插入 Planet
                    planet = Planet(
                        pl_name=row['pl_name'],
                        discoverymethod=row['discoverymethod'],
                        disc_year=int(row['disc_year']) if row['disc_year'] else None,
                        disc_facility=row['disc_facility'],
                        host_star_id=host_star.id
                    )
                    db.session.add(planet)
                    success_count += 1
                except Exception as e:
                    print(f"[第{idx}行] 导入失败: {e}\n数据: {row}")
                    fail_count += 1
            db.session.commit()
        print(f'CSV 导入完成: 成功 {success_count} 条, 失败 {fail_count} 条')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import planet CSV data into the database.')
    parser.add_argument('--csv', type=str, default=DEFAULT_CSV, help='Path to the CSV file')
    args = parser.parse_args()
    import_csv(args.csv)
