import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def save_plot(fig, filename: str) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)


def plot_distribution(df: pd.DataFrame, column: str, output_dir: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df[column], kde=True, ax=ax, color='teal')
    ax.set_title(f'Distribution of {column}')
    save_plot(fig, os.path.join(output_dir, f'{column}_distribution.png'))


def plot_count(df: pd.DataFrame, column: str, output_dir: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x=column, palette='muted', ax=ax)
    ax.set_title(f'{column} Count')
    save_plot(fig, os.path.join(output_dir, f'{column}_count.png'))


def plot_correlation(df: pd.DataFrame, output_dir: str) -> None:
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('Feature Correlation Matrix')
    save_plot(fig, os.path.join(output_dir, 'correlation_matrix.png'))


def main():
    from src.models.data_utils import get_data_path, load_data

    df = load_data(get_data_path())
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    os.makedirs(output_dir, exist_ok=True)

    plot_count(df, 'Exited', output_dir)
    plot_correlation(df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], errors='ignore'), output_dir)
    plot_distribution(df, 'Age', output_dir)
    plot_distribution(df, 'Balance', output_dir)
    plot_distribution(df, 'EstimatedSalary', output_dir)

    print(f'EDA images saved to {output_dir}')


if __name__ == '__main__':
    main()
