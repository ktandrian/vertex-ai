"""
This module defines the category map for expense classification.
"""

CATEGORIES_MAP = {
    "Phone-mobile_Internet-and-telephone": {
        "Category Claim": "Phone/mobile",
        "Sub Category": "Internet and telephone",
        "COA": "511002",
        "Category Description": "mobile allowance",
    },
    "Business-Travel_Travel-Overseas-Flight": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Overseas - Flight",
        "COA": "508001",
        "Category Description": "International travel - flight and visa",
    },
    "Business-Travel_Travel-Overseas-Accom": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Overseas - Accom",
        "COA": "508002",
        "Category Description": "International travel - accomodation, laundry and data roaming",
    },
    "Business-Travel_Travel-Overseas-Ground-Transport": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Overseas - Ground Transport",
        "COA": "508003",
        "Category Description": "International travel - ground transport",
    },
    "Business-Travel_Travel-Overseas-Per-Diem": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Overseas - Per Diem",
        "COA": "508004",
        "Category Description": "International travel - per diem",
    },
    "Business-Travel_Travel-Domestic-Flight": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Domestic - Flight",
        "COA": "508005",
        "Category Description": "Domestic travel - flight",
    },
    "Business-Travel_Travel-Domestic-Accom": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Domestic - Accom",
        "COA": "508006",
        "Category Description": "Domestic travel - accomodation and laundry",
    },
    "Business-Travel_Travel-Domestic-Per-Diem": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Domestic - Per Diem",
        "COA": "508007",
        "Category Description": "Domestic travel - per diem",
    },
    "Business-Travel_Travel-Domestic-Ground-Transport": {
        "Category Claim": "Business Travel",
        "Sub Category": "Travel - Domestic - Ground Transport",
        "COA": "508008",
        "Category Description": "Domestic travel - ground transportation",
    },
    "Business-Meeting_Entertainment-Gift": {
        "Category Claim": "Business Meeting",
        "Sub Category": "Entertainment & Gift",
        "COA": "506202",
        "Category Description": "Business meals with partner",
    },
    "Gifts-to-Partner_Entertainment-Gift": {
        "Category Claim": "Gifts to Partner",
        "Sub Category": "Entertainment & Gift",
        "COA": "506202",
        "Category Description": "Gift to partner",
    },
    "Cash-Advance_Advance-Payment-Employee-current": {
        "Category Claim": "Cash Advance",
        "Sub Category": "Advance Payment Employee - current",
        "COA": "117205",
        "Category Description": "Travel advances",
    },
    "Courier-Services_Postage-and-courier": {
        "Category Claim": "Courier Services",
        "Sub Category": "Postage and courier",
        "COA": "512003",
        "Category Description": "Courier services for Group operation",
    },
    "Duty-Stamp-Meterai_Postage-and-courier": {
        "Category Claim": "Duty Stamp (Meterai)",
        "Sub Category": "Postage and courier",
        "COA": "512003",
        "Category Description": "Duty stamps",
    },
    "Eats-Delivery_Food-and-beverages": {
        "Category Claim": "Eats Delivery",
        "Sub Category": "Food and beverages",
        "COA": "512013",
        "Category Description": "",
    },
    "Food-Beverage_Food-and-beverages": {
        "Category Claim": "Food & Beverage",
        "Sub Category": "Food and beverages",
        "COA": "512013",
        "Category Description": "Claim of meals for OT & special events (livestream, etc.)",
    },
    "Legal-Fee_Legal-fees": {
        "Category Claim": "Legal Fee",
        "Sub Category": "Legal fees",
        "COA": "509001",
        "Category Description": "Professional fees for legal advices and documentations",
    },
    "Office-Supplies_Office-supplies-and-printing": {
        "Category Claim": "Office Supplies",
        "Sub Category": "Office supplies and printing",
        "COA": "512002",
        "Category Description": "Stationaries and printing costs",
    },
    "Permits-Licenses_Permit-Business-licences-fees": {
        "Category Claim": "Permits/Licenses",
        "Sub Category": "Permit/Business licences fees",
        "COA": "509007",
        "Category Description": "Permit/business license fees",
    },
    "Petty-Cash_Depends-of-the-settlement-expenses": {
        "Category Claim": "Petty Cash",
        "Sub Category": "Depends of the settlement expenses",
        "COA": None,  # Special case: COA must be determined later
        "Category Description": "Petty cash settlement",
    },
    "Purchase-Testing_Ticket-testing": {
        "Category Claim": "Purchase Testing",
        "Sub Category": "Ticket testing",
        "COA": "403020",
        "Category Description": (
            "Cost incurred by BU for testing the system/integration with biz partner "
            "in which the company really pays the booking to biz partner"
        ),
    },
    "Software-Subscription_Software-subcriptions-fees": {
        "Category Claim": "Software Subscription",
        "Sub Category": "Software subcriptions fees",
        "COA": "507002",
        "Category Description": "Software subcriptions fees for Group operations",
    },
    "Team-Lunch-Dinner_Food-and-beverages": {
        "Category Claim": "Team Lunch/Dinner",
        "Sub Category": "Food and beverages",
        "COA": "512013",
        "Category Description": "",
    },
    "Transportation_Travel-Domestic-Ground-Transport": {
        "Category Claim": "Transportation",
        "Sub Category": "Travel - Domestic - Ground Transport",
        "COA": "508008",
        "Category Description": "Claim of transport for OT and Group operations",
    },
    "Employee-Loan_Loan-receivables-third-party-current": {
        "Category Claim": "Employee Loan",
        "Sub Category": "Loan receivables third party - current",
        "COA": "117401",
        "Category Description": "Employee loan during COVID period",
    },
    "Team-Engagement_Employee-Welfare": {
        "Category Claim": "Team Engagement",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Team engagement, Community, Country Engangement",
    },
    "Accommodation-Rental_Employee-Welfare": {
        "Category Claim": "Accommodation Rental",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "",
    },
    "Bereavement-Benefits_Employee-Welfare": {
        "Category Claim": "Bereavement Benefits",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Bereavement benefits for employee",
    },
    "Employee-welfare_Employee-Welfare": {
        "Category Claim": "Employee welfare",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": (
            "other employee's benefit that does not cover in other sub-category"
        ),
    },
    "Gifts-to-Employee_Employee-Welfare": {
        "Category Claim": "Gifts to Employee",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Gift to employee for baby born, wedding & medical leave",
    },
    "Housing-Allowance_Employee-Welfare": {
        "Category Claim": "Housing Allowance",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Housing allowance",
    },
    "Medical-Benefits_Medical-expenses": {
        "Category Claim": "Medical Benefits",
        "Sub Category": "Medical expenses",
        "COA": "504005",
        "Category Description": "Medical reimbursement (IN only)",
    },
    "Rapid-Test_Medical-expenses": {
        "Category Claim": "Rapid Test",
        "Sub Category": "Medical expenses",
        "COA": "504005",
        "Category Description": "Rapid test during COVID period",
    },
    "Training_Training-employee": {
        "Category Claim": "Training",
        "Sub Category": "Training employee",
        "COA": "504008",
        "Category Description": "Training costs",
    },
    "Travel-Allowance_Employee-Welfare": {
        "Category Claim": "Travel Allowance",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Lifestyle allowance (IN & PH only)",
    },
    "Tuition-Allowance_Employee-Welfare": {
        "Category Claim": "Tuition Allowance",
        "Sub Category": "Employee Welfare",
        "COA": "504006",
        "Category Description": "Tuition allowance for employee's child",
    },
    # --- Default / Fallback Category ---
    "Default_Uncategorized": {
        "Category Claim": "Uncategorized",
        "Sub Category": "Needs Review",
        "COA": "999999",
        "Category Description": (
            "Item could not be automatically classified and requires manual review."
        ),
    },
}


def categorize_expense(classification_key: str, raw_expense_item: dict) -> dict:
    """
    Performs the deterministic mapping of a classification key to the full category data.

    This function is the second step in the workflow, taking the key chosen by the AI
    and mapping it to the ground-truth data in the FINAL_CATEGORIES_MAP.

    Args:
        classification_key: The unique category key returned by the Gemini model
                            (e.g., "Business-Travel_Travel-Overseas-Flight").
        raw_expense_item: The dictionary containing the original, unprocessed data
                          for a single expense item (merchant, description, amount, etc.).

    Returns:
        The updated expense item dictionary, now enriched with the final, correct
        'Category Claim', 'Sub Category', 'COA', and 'Category Description'.
    """
    # Use .get() for a safe lookup. If the key from Gemini is invalid or not found,
    # it will fall back to the 'Default_Uncategorized' entry. This makes the system robust.
    category_details = CATEGORIES_MAP.get(
        classification_key, CATEGORIES_MAP["Default_Uncategorized"]
    )

    # Use .update() to merge the looked-up category details into the original item.
    # This modifies the dictionary in-place.
    raw_expense_item.update(category_details)

    return raw_expense_item
