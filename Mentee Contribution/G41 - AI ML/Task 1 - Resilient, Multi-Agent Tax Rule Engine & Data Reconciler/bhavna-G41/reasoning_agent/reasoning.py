
def generate_reasoning(asset_data, rules_data, calculation_result):
    """
    Generate human-readable explanations for tax calculations.
    """

    asset_name = calculation_result.get(
        "asset_name",
        asset_data.get("asset_name", "Unknown")
    )

    jurisdiction = calculation_result.get(
        "jurisdiction",
        asset_data.get("jurisdiction", "Unknown")
    )

    rule_id = calculation_result.get("rule_id")
    status = calculation_result.get("status")

    # Find matching tax rule
    rules = rules_data.get("rules", [])
    matched_rule = next(
        (
            rule for rule in rules
            if rule.get("rule_id") == rule_id
        ),
        None
    )

    law_reference = rules_data.get(
        "law_reference",
        "Not specified"
    )

    rule_source = (
        matched_rule.get("source", "Not specified")
        if matched_rule else "Not specified"
    )

    reasoning = []

    requires_review = (
        status != "calculated"
        or calculation_result.get("requires_review", False)
    )

    # CASE 1: Successful calculation
    if status == "calculated":

        method = calculation_result.get("method", "Not specified")

        original_cost = calculation_result.get(
            "original_cost",
            asset_data.get("purchase_cost", 0)
        )

        depreciation_amount = calculation_result.get(
            "depreciation_amount", 0
        )

        depreciation_rate = calculation_result.get(
            "depreciation_rate"
        )

        # India uses closing_wdv; US uses remaining_basis
        closing_value = calculation_result.get(
            "closing_wdv",
            calculation_result.get("remaining_basis")
        )

        reasoning.append(
            f"Asset '{asset_name}' was successfully classified."
        )

        reasoning.append(
            f"Applicable jurisdiction: {jurisdiction}."
        )

        reasoning.append(
            f"Tax depreciation method used: {method}."
        )

        reasoning.append(
            f"Original asset cost: {original_cost}."
        )

        if depreciation_rate is not None:
            reasoning.append(
                f"Depreciation rate: {depreciation_rate * 100:.2f}%."
            )

        reasoning.append(
            f"Depreciation amount: {depreciation_amount}."
        )

        if closing_value is not None:
            value_label = (
                "Closing written down value"
                if method == "WDV"
                else "Remaining depreciable basis"
            )

            reasoning.append(
                f"{value_label}: {closing_value}."
            )

        reasoning.append(
            f"Applicable tax reference: {law_reference}."
        )

        if rule_source != "Not specified":
            reasoning.append(
                f"Rule source: {rule_source}."
            )

        if requires_review:
            review_reason = calculation_result.get(
                "review_reason",
                "Additional verification is required."
            )

            reasoning.append(
                f"Review warning: {review_reason}"
            )

            summary = (
                "Tax depreciation was calculated, "
                "but additional review is required."
            )
        else:
            summary = (
                "Tax depreciation was calculated successfully."
            )

    # CASE 2: Manual review required
    elif status == "manual_review":

        review_reason = calculation_result.get(
            "reason",
            "Additional verification is required."
        )

        reasoning.append(
            f"Asset '{asset_name}' requires manual review."
        )

        reasoning.append(
            f"Jurisdiction: {jurisdiction}."
        )

        reasoning.append(
            f"Reason: {review_reason}"
        )

        reasoning.append(
            f"Applicable rule: {rule_id or 'Not identified'}."
        )

        reasoning.append(
            f"Applicable tax reference: {law_reference}."
        )

        summary = (
            "Tax calculation requires manual verification."
        )

    # CASE 3: Calculation error or unknown status
    else:

        error_reason = calculation_result.get(
            "reason",
            "Unknown calculation error."
        )

        reasoning.append(
            f"Tax calculation could not be completed for '{asset_name}'."
        )

        reasoning.append(
            f"Jurisdiction: {jurisdiction}."
        )

        reasoning.append(
            f"Error details: {error_reason}"
        )

        summary = (
            "Tax calculation failed. "
            "Manual investigation is required."
        )

    # Final reasoning response
    output = {
        "agent": "Reasoning Agent",
        "asset_name": asset_name,
        "jurisdiction": jurisdiction,
        "rule_id": rule_id,
        "law_reference": law_reference,
        "status": status,
        "summary": summary,
        "reasoning": reasoning,
        "requires_review": requires_review
    }

    return output
