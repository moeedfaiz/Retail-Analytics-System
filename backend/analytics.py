# ==========================================================
# Retail Analytics
# ==========================================================

def generate_analytics(nestle_boxes, other_boxes):
    """
    Generates analytics for dashboard.

    Returns:
        dict
    """

    nestle_count = len(nestle_boxes)
    other_count = len(other_boxes)

    total = nestle_count + other_count

    if total == 0:
        nestle_percentage = 0
        other_percentage = 0
    else:
        nestle_percentage = round((nestle_count / total) * 100, 2)
        other_percentage = round((other_count / total) * 100, 2)

    analytics = {

        # ==========================
        # Summary Cards
        # ==========================

        "summary": {

            "total_products": total,
            "nestle_products": nestle_count,
            "other_products": other_count,
            "nestle_share": nestle_percentage,
            "other_share": other_percentage
        },

        # ==========================
        # Pie Chart
        # ==========================

        "pie_chart": [

            {
                "name": "Nestlé",
                "value": nestle_count
            },

            {
                "name": "Other",
                "value": other_count
            }

        ],

        # ==========================
        # Bar Chart
        # ==========================

        "bar_chart": [

            {
                "category": "Nestlé",
                "count": nestle_count
            },

            {
                "category": "Other",
                "count": other_count
            }

        ],

        # ==========================
        # Dashboard Stats
        # ==========================

        "stats": {

            "Nestlé %": nestle_percentage,
            "Other %": other_percentage

        }

    }

    return analytics


# ==========================================================
# Console Report
# ==========================================================

def print_report(analytics):
    """
    Prints analytics to terminal.
    """

    summary = analytics["summary"]

    print("\n==============================")
    print("      RETAIL ANALYTICS")
    print("==============================")

    print(f"Total Products : {summary['total_products']}")
    print(f"Nestlé Products: {summary['nestle_products']}")
    print(f"Other Products : {summary['other_products']}")

    print("------------------------------")

    print(f"Nestlé Share : {summary['nestle_share']}%")
    print(f"Other Share  : {summary['other_share']}%")

    print("==============================\n")