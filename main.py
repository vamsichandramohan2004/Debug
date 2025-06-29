from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
# Corrected imports to include all agents and tasks
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification


app = FastAPI(title="Blood Test Report Analyser")

# Corrected: Ensure file_path is passed into kickoff
def run_crew(query: str, file_path: str): # Removed default as it will always be passed from /analyze
    """To run the whole crew"""
    medical_crew = Crew(
        # Included all agents
        agents=[doctor, verifier, nutritionist, exercise_specialist],
        # Included all tasks
        tasks=[help_patients, nutrition_analysis, exercise_planning, verification],
        process=Process.sequential,
    )
    
    # CORRECTED LINE HERE: Pass the actual file_path to the kickoff inputs
    result = medical_crew.kickoff(inputs={'query': query, 'file_path': file_path}) # Pass the actual file_path
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        # Pass the dynamically created file_path to run_crew
        response = run_crew(query=query.strip(), file_path=file_path) # This call was already correct
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log the error if cleanup fails
                print(f"Error cleaning up file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)