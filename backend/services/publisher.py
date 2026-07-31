import json
import os
from datetime import datetime


def publish_tkp(tkp: dict):

    os.makedirs("samples", exist_ok=True)

    title = tkp.get(
        "metadata",
        {}
    ).get(
        "topic",
        "TeacherKnowledgePackage"
    )

    safe_name = "".join(
        c if c.isalnum() or c in " _-" else "_"
        for c in title
    )

    safe_name = safe_name.replace(" ", "_")

    filename = f"TeacherKnowledgePackage_{safe_name}.json"

    filepath = os.path.join(
        "samples",
        filename
    )

    tkp["generated_at"] = datetime.now().isoformat()

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tkp,
            file,
            indent=2,
            ensure_ascii=False
        )

    return {
        "filename": filename,
        "path": filepath
    }