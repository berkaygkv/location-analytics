import papermill as pm
import sys
import os

path = __file__
path = path.replace(path.split('/')[-1], '')
city_name = sys.argv[1]
os.chdir('..')
print(os.getcwd())
print(city_name)
report_path = f'reports/cities/{city_name}'
if not os.path.exists(report_path):
    os.mkdir(report_path)
    print(f'{report_path} dir created.')

else:
    print('Directory found.')

pm.execute_notebook('notebooks/geo_clustering_nb.ipynb',
                    f'{report_path}/geo_clustering_nb_{city_name}.ipynb',
                    parameters={
                        'city_name': city_name
                    }, 
                    report_mode=True, request_save_on_cell_execute=False)

target_nb = f'{report_path}/geo_clustering_nb_{city_name}.ipynb'
target_html = f'geo_clustering_nb_{city_name}.html'
os.system(f'jupyter nbconvert "{target_nb}" --to html --no-input --output "{target_html}"')