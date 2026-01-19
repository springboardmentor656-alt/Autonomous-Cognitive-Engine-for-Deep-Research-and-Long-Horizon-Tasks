"""
Upload test dataset to LangSmith for UI-based evaluation.
This creates a "Dataset" you can use in the LangSmith dashboard.
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langsmith import Client
from tests.test_dataset import MILESTONE_1_TEST_CASES
from config.settings import settings

def upload_dataset_to_langsmith():
    """
    Upload test cases to LangSmith as a Dataset.
    This allows you to:
    1. View all test cases in the LangSmith UI
    2. Run experiments with one click
    3. Use LLM-as-a-judge evaluation
    """
    
    print("=" * 70)
    print("UPLOADING DATASET TO LANGSMITH")
    print("=" * 70)
    
    client = Client()
    
    dataset_name = "financial-planning-milestone2"

    try:
        existing = client.read_dataset(dataset_name=dataset_name)
        print(f"\nDataset '{dataset_name}' already exists.")
        response = input("Do you want to delete and recreate it? (yes/no): ")
        
        if response.lower() == 'yes':
            client.delete_dataset(dataset_name=dataset_name)
            print("Deleted existing dataset")
        else:
            print("Cancelled. Exiting.")
            return
    except:
        pass
    
    print(f"\nCreating dataset: {dataset_name}")
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Test cases for evaluating financial planning task decomposition (Milestone 1)"
    )
    
    print(f"\nUploading {len(MILESTONE_1_TEST_CASES)} test cases...")
    
    for i, test_case in enumerate(MILESTONE_1_TEST_CASES, 1):
        inputs = {
            "user_request": test_case['prompt'],
            "category": test_case['category']
        }
        
        outputs = {
            "expected_tasks": test_case['expected_tasks'],
            "test_id": test_case['id']
        }
        
        client.create_example(
            inputs=inputs,
            outputs=outputs,
            dataset_id=dataset.id
        )
        
        print(f"  [{i}/{len(MILESTONE_1_TEST_CASES)}] Uploaded: {test_case['category']}")
    
    print("\n" + "=" * 70)
    print("DATASET UPLOAD COMPLETE")
    print("=" * 70)
    print(f"\nView your dataset in LangSmith:")
    print(f"   https://smith.langchain.com/")
    print(f"\nDataset name: {dataset_name}")
    print(f"   Examples: {len(MILESTONE_1_TEST_CASES)}")
    print("\nNext steps:")
    print("   1. Go to LangSmith dashboard")
    print("   2. Click 'Datasets' in left sidebar")
    print("   3. Find your dataset: 'financial-planning-milestone1'")
    print("   4. Click 'Test' to run an experiment!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        settings.validate()
        upload_dataset_to_langsmith()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure your LANGCHAIN_API_KEY is set in .env file")