// src/components/ResultViewer.jsx

export default function ResultViewer({ result }) {
  if (!result) return null;

  // -----------------------------------------
  // Handle new 10-stage backend structure
  // -----------------------------------------

  const metadata = result.metadata || {};
  const knowledge = result.knowledge || {};

  const title =
    knowledge.title ||
    metadata.topic ||
    "Teacher Knowledge Package";

  const summary =
    knowledge.summary ||
    "No summary available.";

  const learningObjectives =
    knowledge.learning_objectives || [];

  const keyConcepts =
    knowledge.key_concepts || [];

  const prerequisites =
    knowledge.prerequisites || [];

  const examples =
    knowledge.examples || [];

  const misconceptions =
    knowledge.misconceptions || [];

  const activities =
    result.activities?.activities ||
    result.activities ||
    knowledge.activities ||
    [];

  const assessment =
    result.assessment || {};

  const difficulty =
    knowledge.difficulty_level ||
    metadata.difficulty ||
    "Not specified";

  const teachingTime =
    knowledge.estimated_teaching_time ||
    "Not specified";


  // -----------------------------------------
  // Download JSON
  // -----------------------------------------

  const downloadJSON = () => {

    const jsonString = JSON.stringify(
      result,
      null,
      2
    );

    const blob = new Blob(
      [jsonString],
      {
        type: "application/json",
      }
    );

    const url =
      URL.createObjectURL(blob);

    const link =
      document.createElement("a");

    link.href = url;

    link.download =
      `${getShortTitle(title)}.json`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };


  // -----------------------------------------
  // Helper for arrays
  // -----------------------------------------

  const renderList = (items, emptyText) => {

    if (!items || items.length === 0) {
      return (
        <p className="empty-text">
          {emptyText}
        </p>
      );
    }

    return (
      <ul>
        {items.map((item, index) => {

          // Handle string
          if (typeof item === "string") {
            return (
              <li key={index}>
                {item}
              </li>
            );
          }

          // Handle activity/object
          if (typeof item === "object") {

            return (
              <li key={index}>

                {item.name && (
                  <strong>
                    {item.name}
                  </strong>
                )}

                {item.question && (
                  <strong>
                    {item.question}
                  </strong>
                )}

                {item.concept && (
                  <strong>
                    {item.concept}
                  </strong>
                )}

                {item.instructions && (
                  <div>
                    <strong>
                      Instructions:
                    </strong>

                    <ul>
                      {item.instructions.map(
                        (instruction, i) => (
                          <li key={i}>
                            {instruction}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

                {item.answer && (
                  <p>
                    <strong>
                      Answer:
                    </strong>{" "}
                    {item.answer}
                  </p>
                )}

                {item.explanation && (
                  <p>
                    <strong>
                      Explanation:
                    </strong>{" "}
                    {item.explanation}
                  </p>
                )}

                {item.solution && (
                  <p>
                    <strong>
                      Solution:
                    </strong>{" "}
                    {item.solution}
                  </p>
                )}

                {item.gap && (
                  <p>
                    <strong>
                      Gap:
                    </strong>{" "}
                    {item.gap}
                  </p>
                )}

                {item.strategy && (
                  <p>
                    <strong>
                      Strategy:
                    </strong>{" "}
                    {item.strategy}
                  </p>
                )}

              </li>
            );
          }

          return null;
        })}
      </ul>
    );
  };


  return (

    <div className="result-container">

      {/* ================================= */}
      {/* HEADER */}
      {/* ================================= */}

      <div className="result-header">
        <div>
          <span className="eyebrow">
            GENERATED OUTPUT
          </span>
        </div>
      </div>


      {/* ================================= */}
      {/* METADATA */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          📚 Topic
        </h3>

        <p className="result-title">
          {title}
        </p>

        {metadata.subject && (
          <p>
            <strong>
              Subject:
            </strong>{" "}
            {metadata.subject}
          </p>
        )}

      </section>

      {/* ================================= */}
      {/* SUMMARY */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          📝 Summary
        </h3>

        <p>
          {summary}
        </p>

      </section>


      {/* ================================= */}
      {/* LEARNING OBJECTIVES */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          🎯 Learning Objectives
        </h3>

        {renderList(
          learningObjectives,
          "No learning objectives available."
        )}

      </section>


      {/* ================================= */}
      {/* KEY CONCEPTS */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          🧠 Key Concepts
        </h3>

        {renderList(
          keyConcepts,
          "No key concepts available."
        )}

      </section>


      {/* ================================= */}
      {/* PREREQUISITES */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          📌 Prerequisites
        </h3>

        {renderList(
          prerequisites,
          "No prerequisites available."
        )}

      </section>


      {/* ================================= */}
      {/* EXAMPLES */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          💡 Examples
        </h3>

        {renderList(
          examples,
          "No examples available."
        )}

      </section>


      {/* ================================= */}
      {/* MISCONCEPTIONS */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          ⚠️ Common Misconceptions
        </h3>

        {renderList(
          misconceptions,
          "No misconceptions available."
        )}

      </section>


      {/* ================================= */}
      {/* TEACHING PLAN */}
      {/* ================================= */}

      {result.teaching_plan && (

        <section className="result-block">

          <h3>
            👨‍🏫 Teaching Plan
          </h3>

          {result.teaching_plan.total_periods && (

            <p>
              <strong>
                Total Periods:
              </strong>{" "}
              {result.teaching_plan.total_periods}
            </p>

          )}

          {result.teaching_plan.periods && (

            <div>

              {result.teaching_plan.periods.map(
                (period, index) => (

                  <div
                    key={index}
                    className="period-card"
                  >

                    <h4>
                      Period {period.period}
                    </h4>

                    <p>
                      <strong>
                        Topic:
                      </strong>{" "}
                      {period.topic}
                    </p>

                    <p>
                      <strong>
                        Duration:
                      </strong>{" "}
                      {period.duration}
                    </p>

                    {period.objectives && (

                      <div>

                        <strong>
                          Objectives:
                        </strong>

                        {renderList(
                          period.objectives,
                          ""
                        )}

                      </div>

                    )}

                  </div>

                )
              )}

            </div>

          )}

        </section>

      )}


      {/* ================================= */}
      {/* CLASSROOM CONTENT */}
      {/* ================================= */}

      {result.classroom_content && (

        <section className="result-block">

          <h3>
            🏫 Classroom Content
          </h3>

          {result.classroom_content.entry_ticket && (

            <>
              <h4>
                🎫 Entry Ticket
              </h4>

              {renderList(
                result.classroom_content.entry_ticket,
                "No entry ticket available."
              )}
            </>

          )}

          {result.classroom_content.teacher_script && (

            <>
              <h4>
                🗣️ Teacher Script
              </h4>

              {renderList(
                result.classroom_content.teacher_script,
                "No teacher script available."
              )}
            </>

          )}

          {result.classroom_content.board_notes && (

            <>
              <h4>
                📝 Board Notes
              </h4>

              {renderList(
                result.classroom_content.board_notes,
                "No board notes available."
              )}
            </>

          )}

          {result.classroom_content.exit_ticket && (

            <>
              <h4>
                🚪 Exit Ticket
              </h4>

              {renderList(
                result.classroom_content.exit_ticket,
                "No exit ticket available."
              )}
            </>

          )}

          {result.classroom_content.homework && (

            <>
              <h4>
                📖 Homework
              </h4>

              {renderList(
                result.classroom_content.homework,
                "No homework available."
              )}
            </>

          )}

        </section>

      )}


      {/* ================================= */}
      {/* ACTIVITIES */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          🧪 Activities
        </h3>

        {renderList(
          activities,
          "No activities available."
        )}

      </section>


      {/* ================================= */}
      {/* ASSESSMENT */}
      {/* ================================= */}

      <section className="result-block">

        <h3>
          📊 Assessment
        </h3>


        {assessment.mcqs && (

          <>

            <h4>
              Multiple Choice Questions
            </h4>

            {renderList(
              assessment.mcqs,
              "No MCQs available."
            )}

          </>

        )}


        {assessment.short_answer && (

          <>

            <h4>
              Short Answer
            </h4>

            {renderList(
              assessment.short_answer,
              "No short-answer questions."
            )}

          </>

        )}


        {assessment.long_answer && (

          <>

            <h4>
              Long Answer
            </h4>

            {renderList(
              assessment.long_answer,
              "No long-answer questions."
            )}

          </>

        )}


        {assessment.numerical && (

          <>

            <h4>
              Numerical Problems
            </h4>

            {renderList(
              assessment.numerical,
              "No numerical problems."
            )}

          </>

        )}

      </section>


      {/* ================================= */}
      {/* LEARNING GAP ANALYSIS */}
      {/* ================================= */}

      {result.learning_gap_analysis && (

        <section className="result-block">

          <h3>
            🔍 Learning Gap Analysis
          </h3>


          {result.learning_gap_analysis
            .diagnostic_questions && (

            <>

              <h4>
                Diagnostic Questions
              </h4>

              {renderList(
                result.learning_gap_analysis
                  .diagnostic_questions,
                "No diagnostic questions."
              )}

            </>

          )}


          {result.learning_gap_analysis
            .common_gaps && (

            <>

              <h4>
                Common Learning Gaps
              </h4>

              {renderList(
                result.learning_gap_analysis
                  .common_gaps,
                "No learning gaps identified."
              )}

            </>

          )}


          {result.learning_gap_analysis
            .remediation && (

            <>

              <h4>
                Remediation
              </h4>

              {renderList(
                result.learning_gap_analysis
                  .remediation,
                "No remediation strategies."
              )}

            </>

          )}

        </section>

      )}


      {/* ================================= */}
      {/* METADATA */}
      {/* ================================= */}

      <div className="result-meta">

        <div>

          <span>
            Difficulty
          </span>

          <strong>
            {difficulty}
          </strong>

        </div>


        <div>

          <span>
            Teaching Time
          </span>

          <strong>
            {teachingTime}
          </strong>

        </div>

      </div>


      {/* ================================= */}
      {/* DOWNLOAD */}
      {/* ================================= */}

      <div className="download-area">

        <p>
          Save this Teacher Knowledge Package
          for later use.
        </p>

        <button
          className="download-button large"
          onClick={downloadJSON}
        >
          ↓ Download{" "}
          {getShortTitle(title)}.json
        </button>

      </div>

    </div>
  );
}


// =========================================
// File name helper
// =========================================

function getShortTitle(title) {

  if (!title) {
    return "TeacherKnowledgePackage";
  }

  return title
    .replace(/[^a-zA-Z0-9\s-]/g, "")
    .trim()
    .replace(/\s+/g, "_")
    .slice(0, 80);
}