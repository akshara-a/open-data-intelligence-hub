import os
import subprocess


def main():
    project_root = os.path.dirname(__file__)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    filename = os.path.join(data_dir, 'Churn_Modelling.csv')
    if os.path.exists(filename):
        print(f'Dataset already exists at {filename}')
        return

    print('Downloading Bank Customer Churn dataset from Kaggle...')
    command = [
        'kaggle',
        'datasets',
        'download',
        '-d',
        'sagnik1511/churn-modelling',
        '-f',
        'Churn_Modelling.csv',
        '-p',
        data_dir,
        '--unzip',
    ]
    subprocess.run(command, check=True)
    print(f'Dataset downloaded to {data_dir}')


if __name__ == '__main__':
    main()
