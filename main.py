import sys
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "src"))

from src.graph.workflow import app

def run_research(topic: str):
    inputs = {
        "topic": topic,
        "revision_count": 0,
        "research_data": [],
        "critique": "",
        "report": "" 
    }
    
    print(f"🚀 AGENT STARTED: {topic}")
    
    try:
        # Execute Graph
        final_state = app.invoke(inputs)
        
        # Get the report
        report = final_state.get("report", "")
        
        if report:
            print("\n✅ RESEARCH COMPLETE! GENERATING FILE...")
            
            # Save to Markdown file
            output_path = os.path.join(BASE_DIR, "final_report.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"📄 Report saved to: {output_path}")
            print("\n--- REPORT PREVIEW ---")
            print(report[:500] + "...") # Show first 500 chars
        else:
            print("❌ Failure: No report content found in the final state.")
            
    except Exception as e:
        print(f"❌ EXECUTION ERROR: {e}")

if __name__ == "__main__":
    run_research("The impact of covid-19 on global supply chains")