def validate_tkp(tkp):

    required_fields = [
        "metadata",
        "knowledge",
        "teaching_plan",
        "classroom_content",
        "activities",
        "assessment",
        "learning_gap_analysis"
    ]

    errors = []

    for field in required_fields:

        if field not in tkp:
            errors.append(
                f"Missing field: {field}"
            )

    if "knowledge" in tkp:

        required_knowledge = [
            "summary",
            "learning_objectives",
            "key_concepts",
            "prerequisites",
            "examples",
            "misconceptions"
        ]

        for field in required_knowledge:

            if field not in tkp["knowledge"]:

                errors.append(
                    f"Missing knowledge field: {field}"
                )

    if "learning_objectives" in tkp.get("knowledge", {}):

        if not isinstance(
            tkp["knowledge"]["learning_objectives"],
            list
        ):
            errors.append(
                "learning_objectives must be a list"
            )

    if errors:

        raise ValueError(
            "TKP validation failed: "
            + "; ".join(errors)
        )

    return {
        "valid": True,
        "errors": []
    }