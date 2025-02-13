import os
import sys
import subprocess
import config  # Import configuration variables from config.py

def run_script(script_path, project_root):
    """
    Executes a Python script using a modified environment that includes the project root in PYTHONPATH.
    """
    print(f"Running: {script_path}")

    # Copy the current environment and ensure that the project root is in PYTHONPATH.
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    if current_pythonpath:
        env["PYTHONPATH"] = project_root + os.pathsep + current_pythonpath
    else:
        env["PYTHONPATH"] = project_root

    # Run the script with the working directory set to the project root.
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=project_root,
        env=env
    )
    if result.returncode == 0:
        print(result.stdout)
        print(f"{script_path} completed successfully.\n")
    else:
        print(f"Error in {script_path}:")
        print(result.stderr)

def main():
    # Print the configuration from config.py for verification.
    print("Configuration:")
    print("BASE_DIR:", config.BASE_DIR)
    print("Raw Data Directory:", config.RAW_DATA_DIR)
    print("Processed Data Directory:", config.PROCESSED_DATA_DIR)
    print("Visualization Directory:", config.VISUALIZATION_DIR)
    print()

    # Define the project root (where main.py and config.py reside)
    project_root = os.path.dirname(os.path.abspath(__file__))
    # The scripts folder is a subdirectory of the project root.
    scripts_dir = os.path.join(project_root, "scripts")

    # List of extraction scripts.
    extraction_scripts = [
        "collect_binance.py",
        "collect_coingecko.py",
        "collect_fear_greed.py",
        "collect_news.py",
        "collect_reddit.py",
        "collect_yahoo.py"
    ]
    
    # List of preprocessing, visualization, and analysis scripts.
    preprocessing_scripts = [
        "preprocess_data.py"
    ]
    visualization_scripts = [
        "visualization.py"
    ]
    analysis_scripts = [
        "analysis.py"
    ]
    
    print("----- Starting Extraction Phase -----")
    for script in extraction_scripts:
        script_path = os.path.join(scripts_dir, script)
        run_script(script_path, project_root)
    
    print("----- Starting Preprocessing Phase -----")
    for script in preprocessing_scripts:
        script_path = os.path.join(scripts_dir, script)
        run_script(script_path, project_root)
    
    print("----- Starting Visualization Phase -----")
    for script in visualization_scripts:
        script_path = os.path.join(scripts_dir, script)
        run_script(script_path, project_root)
    
    print("----- Starting Analysis Phase -----")
    for script in analysis_scripts:
        script_path = os.path.join(scripts_dir, script)
        run_script(script_path, project_root)
    
    print("----- Pipeline Execution Complete -----")

if __name__ == "__main__":
    main()