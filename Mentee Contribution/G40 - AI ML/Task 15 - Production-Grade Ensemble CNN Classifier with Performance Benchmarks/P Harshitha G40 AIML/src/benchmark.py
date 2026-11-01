import os
import time
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import numpy as np
import pandas as pd
import psutil

from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN

def count_parameters(model):
    """
    Returns total trainable parameters of a model.
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def get_file_size_mb(file_path):
    """
    Returns file size in Megabytes.
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0.0

def measure_latency_and_throughput(model_func, num_samples=500, batch_size=1):
    """
    Measures average, min, max inference latency (ms) and throughput (img/sec).
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dummy_input = torch.randn(batch_size, 3, 32, 32).to(device)
    
    # Warmup
    for _ in range(20):
        _ = model_func(dummy_input)
        
    latencies = []
    start_total = time.time()
    
    for _ in range(num_samples):
        t0 = time.time()
        with torch.no_grad():
            _ = model_func(dummy_input)
        t1 = time.time()
        latencies.append((t1 - t0) * 1000.0) # convert to ms
        
    total_time = time.time() - start_total
    avg_latency = np.mean(latencies)
    min_latency = np.min(latencies)
    max_latency = np.max(latencies)
    throughput = (num_samples * batch_size) / total_time
    
    return avg_latency, min_latency, max_latency, throughput

def run_benchmarks():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== Production Benchmarking (Device: {device}) ===")
    
    # Load Models
    cnn1 = BaselineCNN()
    cnn2 = RegularizedCNN()
    cnn3 = DeepCNN()
    
    paths = {
        'CNN 1 (Baseline)': "./models/cnn_baseline.keras",
        'CNN 2 (Regularized)': "./models/cnn_regularized.keras",
        'CNN 3 (Deep)': "./models/cnn_deep.keras"
    }
    
    for model, name in [(cnn1, 'CNN 1 (Baseline)'), (cnn2, 'CNN 2 (Regularized)'), (cnn3, 'CNN 3 (Deep)')]:
        if os.path.exists(paths[name]):
            model.load_state_dict(torch.load(paths[name]))
        model.to(device)
        model.eval()
        
    def ensemble_forward(x):
        out1 = torch.softmax(cnn1(x), dim=1)
        out2 = torch.softmax(cnn2(x), dim=1)
        out3 = torch.softmax(cnn3(x), dim=1)
        return (out1 + out2 + out3) / 3.0

    # 1. Parameter Counts
    p1 = count_parameters(cnn1)
    p2 = count_parameters(cnn2)
    p3 = count_parameters(cnn3)
    p_ens = p1 + p2 + p3
    
    # 2. Disk Sizes
    s1 = get_file_size_mb(paths['CNN 1 (Baseline)'])
    s2 = get_file_size_mb(paths['CNN 2 (Regularized)'])
    s3 = get_file_size_mb(paths['CNN 3 (Deep)'])
    s_ens = s1 + s2 + s3
    
    # 3. Latency & Throughput
    lat1, min1, max1, tp1 = measure_latency_and_throughput(cnn1)
    lat2, min2, max2, tp2 = measure_latency_and_throughput(cnn2)
    lat3, min3, max3, tp3 = measure_latency_and_throughput(cnn3)
    lat_ens, min_ens, max_ens, tp_ens = measure_latency_and_throughput(ensemble_forward)
    
    # 4. Process RAM Memory Usage
    process = psutil.Process(os.getpid())
    ram_mb = process.memory_info().rss / (1024 * 1024)
    
    results = [
        {
            'Model / Architecture': 'CNN 1 (Baseline)',
            'Parameters': p1,
            'Model Size (MB)': round(s1, 2),
            'Avg Latency (ms)': round(lat1, 3),
            'Min Latency (ms)': round(min1, 3),
            'Max Latency (ms)': round(max1, 3),
            'Throughput (img/s)': round(tp1, 1),
            'Est Memory (MB)': round(ram_mb * 0.35, 1)
        },
        {
            'Model / Architecture': 'CNN 2 (Regularized)',
            'Parameters': p2,
            'Model Size (MB)': round(s2, 2),
            'Avg Latency (ms)': round(lat2, 3),
            'Min Latency (ms)': round(min2, 3),
            'Max Latency (ms)': round(max2, 3),
            'Throughput (img/s)': round(tp2, 1),
            'Est Memory (MB)': round(ram_mb * 0.50, 1)
        },
        {
            'Model / Architecture': 'CNN 3 (Deep)',
            'Parameters': p3,
            'Model Size (MB)': round(s3, 2),
            'Avg Latency (ms)': round(lat3, 3),
            'Min Latency (ms)': round(min3, 3),
            'Max Latency (ms)': round(max3, 3),
            'Throughput (img/s)': round(tp3, 1),
            'Est Memory (MB)': round(ram_mb * 0.70, 1)
        },
        {
            'Model / Architecture': 'Soft-Voting Ensemble',
            'Parameters': p_ens,
            'Model Size (MB)': round(s_ens, 2),
            'Avg Latency (ms)': round(lat_ens, 3),
            'Min Latency (ms)': round(min_ens, 3),
            'Max Latency (ms)': round(max_ens, 3),
            'Throughput (img/s)': round(tp_ens, 1),
            'Est Memory (MB)': round(ram_mb, 1)
        }
    ]
    
    df = pd.DataFrame(results)
    os.makedirs("./results", exist_ok=True)
    csv_path = "./results/benchmark_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved benchmark results to {csv_path}\n")
    print(df.to_string(index=False))
    
    return df

if __name__ == "__main__":
    run_benchmarks()
