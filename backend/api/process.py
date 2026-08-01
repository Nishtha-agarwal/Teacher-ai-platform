from fastapi import APIRouter, HTTPException

from backend.services.parser import extract_text
from backend.services.chunker import chunk_text
from backend.services.classifier import classify_document
from backend.services.tkp_generator import generate_tkp
from backend.services.teaching_planner import generate_teaching_plan
from backend.services.classroom_generator import generate_classroom_content
from backend.services.activity_generator import generate_activities
from backend.services.assessment_generator import generate_assessment
from backend.services.learning_gap import analyze_learning_gaps
from backend.services.validator import validate_tkp


router = APIRouter(
    prefix="/process",
    tags=["Process"]
)


@router.post("/")
async def process_document(data: dict):

    try:

        path = data["path"]

        print("\n================================")
        print("STARTING TEACHER AI PIPELINE")
        print("================================")

        # ==================================================
        # STAGE 1
        # ==================================================

        print("\nStage 1: Document Intelligence")

        text = extract_text(path)

        print(
            f"Extracted text length: {len(text)}"
        )

        chunks = chunk_text(text)

        print(
            f"Chunks created: {len(chunks)}"
        )

        for i, chunk in enumerate(chunks):

            print(
                f"Chunk {i + 1}: "
                f"{len(chunk.split())} words"
            )

        # ==================================================
        # STAGE 2
        # ==================================================

        print("\nStage 2: Educational Classification")

        classification = classify_document(text)

        print("Classification:")
        print(classification)

        # ==================================================
        # STAGE 3
        # ==================================================

        print("\nStage 3: Knowledge Extraction")

        knowledge = generate_tkp(
            chunks,
            classification
        )

        print(
            "Knowledge extraction completed"
        )

        # ==================================================
        # STAGE 4
        # ==================================================

        print("\nStage 4: Teaching Planner")

        teaching_plan = generate_teaching_plan(
            knowledge,
            classification
        )

        print(
            "Teaching plan generated"
        )

        # ==================================================
        # STAGE 5
        # ==================================================

        print("\nStage 5: Classroom Content Generation")

        classroom_content = generate_classroom_content(
            knowledge,
            teaching_plan,
            classification
        )

        print(
            "Classroom content generated"
        )

        # ==================================================
        # STAGE 6
        # ==================================================

        print("\nStage 6: Activity Generation")

        activities = generate_activities(
            knowledge,
            teaching_plan
        )

        print(
            "Activities generated"
        )

        # ==================================================
        # STAGE 7
        # ==================================================

        print("\nStage 7: Assessment Generation")

        assessment = generate_assessment(
            knowledge,
            teaching_plan
        )

        print(
            "Assessment generated"
        )

        # ==================================================
        # STAGE 8
        # ==================================================

        print("\nStage 8: Learning Gap Analysis")

        learning_gaps = analyze_learning_gaps(
            knowledge,
            assessment
        )

        print(
            "Learning gap analysis completed"
        )

        # ==================================================
        # COMBINE TKP
        # ==================================================

        final_tkp = {

            "metadata": classification,

            "knowledge": knowledge,

            "teaching_plan": teaching_plan,

            "classroom_content": classroom_content,

            "activities": activities,

            "assessment": assessment,

            "learning_gap_analysis": learning_gaps
        }

        # ==================================================
        # STAGE 9
        # ==================================================

        print("\nStage 9: Validation")

        validation = validate_tkp(
            final_tkp
        )

        print(
            "✓ TKP validation successful"
        )

        final_tkp["validation"] = validation

        # ==================================================
        # STAGE 10
        # ==================================================

        print("\nStage 10: Publishing")

        print(
            "✓ Teacher Knowledge Package generated"
        )

        print("\n================================")
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("================================")

        return final_tkp

    except Exception as e:

        print("\n================================")
        print("PIPELINE ERROR")
        print("================================")

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
