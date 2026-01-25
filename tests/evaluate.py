"""
Improved evaluation script - Shows created files!
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import create_agent_graph, run_agent
from src.state import AgentState
from tests.test_scenarios import ALL_TEST_SCENARIOS


def display_files(files: dict, scenario_name: str):
    """Display all files created during a test."""
    print(f"\n{'─'*80}")
    print(f"📁 FILES CREATED IN: {scenario_name}")
    print(f"{'─'*80}")
    
    if not files:
        print("❌ No files created!")
        return
    
    for filename, content in files.items():
        print(f"\n📄 {filename}")
        print(f"{'─'*80}")
        print(f"Size: {len(content)} characters")
        print(f"\nContent Preview (first 200 chars):")
        print(content[:200] + ("..." if len(content) > 200 else ""))
        print(f"{'─'*80}")


def save_files_to_disk(files: dict, scenario_name: str, output_dir: str = "results/files"):
    """Save virtual files to actual disk for inspection."""
    os.makedirs(output_dir, exist_ok=True)
    
    scenario_dir = os.path.join(output_dir, scenario_name.replace(" ", "_"))
    os.makedirs(scenario_dir, exist_ok=True)
    
    for filename, content in files.items():
        filepath = os.path.join(scenario_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"\n💾 Files saved to: {scenario_dir}")


def evaluate_scenario(graph, scenario_name: str, scenario_input: str) -> dict:
    """Evaluate a single test scenario."""
    print(f"\n{'='*80}")
    print(f"Testing: {scenario_name}")
    print(f"{'='*80}\n")
    
    # Initialize fresh state
    state = AgentState(
        messages=[],
        files={},
        intermediate_steps=[]
    )
    
    try:
        # Run the agent
        print("🤖 Agent working...")
        final_state = run_agent(graph, scenario_input, state)
        
        # Extract metrics
        files_created = len(final_state['files'])
        write_file_calls = sum(1 for step in final_state['intermediate_steps'] 
                              if step.get('tool') == 'write_file')
        
        # Count read_file calls from messages
        read_file_calls = 0
        for msg in final_state['messages']:
            msg_str = str(msg.content) if hasattr(msg, 'content') else str(msg)
            if 'read_file' in msg_str.lower() or 'content of' in msg_str.lower():
                read_file_calls += 1
        
        # Success criteria
        used_write = write_file_calls > 0
        used_read = read_file_calls > 0
        created_files = files_created >= 2  # At least 2 files for most tests
        
        success = used_write and created_files
        
        # Print results
        print(f"\n{'─'*80}")
        print(f"📊 RESULTS:")
        print(f"{'─'*80}")
        print(f"✅ Files created: {files_created}")
        print(f"✅ write_file calls: {write_file_calls}")
        print(f"✅ read_file calls: {read_file_calls}")
        print(f"✅ Status: {'✅ PASSED' if success else '❌ FAILED'}")
        
        # Show the files!
        display_files(final_state['files'], scenario_name)
        
        # Save files to disk
        if files_created > 0:
            save_files_to_disk(final_state['files'], scenario_name)
        
        return {
            'scenario': scenario_name,
            'success': success,
            'files_created': files_created,
            'write_calls': write_file_calls,
            'read_calls': read_file_calls,
            'file_list': list(final_state['files'].keys()),
            'files_content': final_state['files']  # Save actual content
        }
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'scenario': scenario_name,
            'success': False,
            'error': str(e),
            'files_created': 0,
            'write_calls': 0,
            'read_calls': 0
        }


def run_evaluation():
    """Run full evaluation suite."""
    
    # Check environment
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: GROQ_API_KEY not found in environment!")
        print("Please create .env file with GROQ_API_KEY=your-key")
        return
    
    print("\n" + "="*80)
    print("MILESTONE 2 EVALUATION: Context Offloading via Virtual File System")
    print("="*80)
    print(f"\nStarting evaluation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running {len(ALL_TEST_SCENARIOS)} test scenarios...\n")
    
    # Create agent graph
    print("Initializing agent graph...")
    try:
        graph = create_agent_graph()
        print("✅ Agent ready\n")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return
    
    # Run all tests
    results = []
    for scenario_name, scenario_input in ALL_TEST_SCENARIOS:
        result = evaluate_scenario(graph, scenario_name, scenario_input)
        results.append(result)
        
        # Pause between tests
        print(f"\n{'='*80}\n")
    
    # Calculate overall metrics
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get('success', False))
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    total_files = sum(r.get('files_created', 0) for r in results)
    total_writes = sum(r.get('write_calls', 0) for r in results)
    total_reads = sum(r.get('read_calls', 0) for r in results)
    
    # Print summary
    print("\n" + "="*80)
    print("📊 EVALUATION SUMMARY")
    print("="*80)
    print(f"\n📈 Overall Statistics:")
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success rate: {success_rate:.1f}%")
    print(f"\n📁 File System Usage:")
    print(f"   Total files created: {total_files}")
    print(f"   Total write_file calls: {total_writes}")
    print(f"   Total read_file calls: {total_reads}")
    
    print(f"\n{'─'*80}")
    print(f"{'Scenario':<40} {'Status':<10} {'Files':<8} {'Writes':<8} {'Reads':<8}")
    print("─"*80)
    for r in results:
        status = "✅ PASS" if r.get('success') else "❌ FAIL"
        files = r.get('files_created', 0)
        writes = r.get('write_calls', 0)
        reads = r.get('read_calls', 0)
        print(f"{r['scenario']:<40} {status:<10} {files:<8} {writes:<8} {reads:<8}")
    
    # Evaluation conclusion
    print("\n" + "="*80)
    if success_rate >= 80:
        print("🎉 MILESTONE 2 EVALUATION: PASSED")
        print(f"   Success rate {success_rate:.1f}% meets the >80% requirement")
    elif success_rate >= 60:
        print("⚠️  MILESTONE 2 EVALUATION: PARTIALLY PASSED")
        print(f"   Success rate {success_rate:.1f}% shows good progress")
    else:
        print("❌ MILESTONE 2 EVALUATION: NEEDS IMPROVEMENT")
        print(f"   Success rate {success_rate:.1f}% below the 80% requirement")
    print("="*80)
    
    print("\n📊 Key Achievements:")
    print(f"   {'✅' if total_files >= 10 else '⚠️ '} Created {total_files} files across all tests")
    print(f"   {'✅' if total_writes >= 10 else '⚠️ '} Used write_file {total_writes} times")
    print(f"   {'✅' if success_rate >= 80 else '⚠️ '} Overall success rate: {success_rate:.1f}%")
    
    print("\n💾 Files Location:")
    print(f"   Virtual files saved to: results/files/")
    print(f"   Each test scenario has its own folder")
    print(f"   You can inspect the actual file contents there!")
    
    print("\n" + "="*80)
    
    # Save detailed results
    save_detailed_results(results, success_rate)


def save_detailed_results(results: list, success_rate: float):
    """Save evaluation results with file contents."""
    os.makedirs('results', exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/evaluation_detailed_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("MILESTONE 2 EVALUATION - DETAILED RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
        f.write(f"Status: {'PASSED' if success_rate >= 80 else 'FAILED'}\n\n")
        
        for r in results:
            f.write(f"\n{'='*80}\n")
            f.write(f"Scenario: {r['scenario']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Success: {r.get('success', False)}\n")
            f.write(f"Files created: {r.get('files_created', 0)}\n")
            f.write(f"write_file calls: {r.get('write_calls', 0)}\n")
            f.write(f"read_file calls: {r.get('read_calls', 0)}\n")
            
            if 'file_list' in r and r['file_list']:
                f.write(f"\nFiles: {', '.join(r['file_list'])}\n")
            
            if 'files_content' in r:
                f.write(f"\n--- FILE CONTENTS ---\n")
                for fname, content in r['files_content'].items():
                    f.write(f"\n[{fname}]\n")
                    f.write(content[:500] + "...\n" if len(content) > 500 else content + "\n")
    
    print(f"\n📝 Detailed results saved to: {filename}")


if __name__ == "__main__":
    run_evaluation()