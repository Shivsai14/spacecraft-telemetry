"""
telemetry_data.py
Hard operational limits + synthetic telemetry passes with operator notes.
"""

# ----------------------------------------------------------------------
# HARD LIMITS — breaching ANY of these forces severity = CRITICAL,
# regardless of what the numeric scoring or LLM reasoning concludes.
# ----------------------------------------------------------------------
HARD_LIMITS = {
    "battery_voltage_v": {"min": 6.5, "max": 8.4, "unit": "V"},
    "battery_temp_c": {"min": -10.0, "max": 45.0, "unit": "C"},
    "bus_voltage_v": {"min": 27.0, "max": 33.0, "unit": "V"},
    "solar_current_a": {"min": 0.0, "max": 12.0, "unit": "A"},
    "link_margin_db": {"min": 3.0, "max": 40.0, "unit": "dB"},
    "attitude_error_deg": {"min": -5.0, "max": 5.0, "unit": "deg"},
}

# Nominal baselines used for z-score calculation (mean, std) per parameter.
# Derived from "normal" pass population — would be recomputed from a
# rolling history in a real system.
NOMINAL_BASELINE = {
    "battery_voltage_v": {"mean": 7.6, "std": 0.15},
    "battery_temp_c": {"mean": 18.0, "std": 4.0},
    "bus_voltage_v": {"mean": 30.0, "std": 0.6},
    "solar_current_a": {"mean": 6.5, "std": 1.2},
    "link_margin_db": {"mean": 12.0, "std": 2.5},
    "attitude_error_deg": {"mean": 0.0, "std": 0.8},
}

# ----------------------------------------------------------------------
# SYNTHETIC PASS RECORDS
# Each record = one downlink pass: numeric telemetry + operator note.
# "history" holds the last few battery voltage readings (oldest->newest)
# for the same parameter, enabling trend/degradation detection.
# ----------------------------------------------------------------------
PASSES = [
    {
        "pass_id": "PASS-001",
        "timestamp": "2026-06-25T03:12:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.62,
            "battery_temp_c": 17.4,
            "bus_voltage_v": 30.1,
            "solar_current_a": 6.8,
            "link_margin_db": 13.2,
            "attitude_error_deg": 0.3,
        },
        "battery_voltage_history": [7.65, 7.63, 7.64, 7.62],
        "operator_note": "Nominal pass, all systems green, nothing to report.",
    },
    {
        "pass_id": "PASS-002",
        "timestamp": "2026-06-25T04:48:00Z",
        "eclipse": True,
        "telemetry": {
            "battery_voltage_v": 6.41,
            "battery_temp_c": 12.1,
            "bus_voltage_v": 28.9,
            "solar_current_a": 0.1,
            "link_margin_db": 9.8,
            "attitude_error_deg": -0.6,
        },
        "battery_voltage_history": [7.55, 7.40, 7.10, 6.41],
        "operator_note": "Battery dipping hard during eclipse exit, watching it closely, may not recover before next pass.",
    },
    {
        "pass_id": "PASS-003",
        "timestamp": "2026-06-25T06:20:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.58,
            "battery_temp_c": 47.3,
            "bus_voltage_v": 30.4,
            "solar_current_a": 7.1,
            "link_margin_db": 14.0,
            "attitude_error_deg": 0.2,
        },
        "battery_voltage_history": [7.60, 7.59, 7.61, 7.58],
        "operator_note": "Crew reports nothing unusual on the console, looks like a routine pass.",
    },
    {
        "pass_id": "PASS-004",
        "timestamp": "2026-06-25T07:55:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.30,
            "battery_temp_c": 19.8,
            "bus_voltage_v": 30.0,
            "solar_current_a": 6.2,
            "link_margin_db": 12.5,
            "attitude_error_deg": 0.4,
        },
        "battery_voltage_history": [7.62, 7.55, 7.48, 7.30],
        "operator_note": "Battery trending down pass over pass, not critical yet but worth flagging for the next shift.",
    },
    {
        "pass_id": "PASS-005",
        "timestamp": "2026-06-25T09:30:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.65,
            "battery_temp_c": 18.2,
            "bus_voltage_v": 30.2,
            "solar_current_a": 6.6,
            "link_margin_db": 2.1,
            "attitude_error_deg": 0.1,
        },
        "battery_voltage_history": [7.63, 7.64, 7.66, 7.65],
        "operator_note": "Comms were a little weak this pass but battery and thermal look perfectly fine.",
    },
    {
        "pass_id": "PASS-006",
        "timestamp": "2026-06-25T11:05:00Z",
        "eclipse": True,
        "telemetry": {
            "battery_voltage_v": 7.10,
            "battery_temp_c": 14.5,
            "bus_voltage_v": 29.6,
            "solar_current_a": 0.0,
            "link_margin_db": 11.0,
            "attitude_error_deg": -0.2,
        },
        "battery_voltage_history": [7.60, 7.45, 7.25, 7.10],
        "operator_note": "Normal eclipse pass, battery dip is expected, no concerns from my side.",
    },
    {
        "pass_id": "PASS-007",
        "timestamp": "2026-06-25T12:40:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.55,
            "battery_temp_c": 19.0,
            "bus_voltage_v": 30.1,
            "solar_current_a": 6.4,
            "link_margin_db": 13.8,
            "attitude_error_deg": 6.4,
        },
        "battery_voltage_history": [7.58, 7.56, 7.57, 7.55],
        "operator_note": "Power and thermal nominal, but attitude sensor seemed jittery on the plots, possibly noise.",
    },
    {
        "pass_id": "PASS-008",
        "timestamp": "2026-06-25T14:15:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.59,
            "battery_temp_c": 18.6,
            "bus_voltage_v": 30.0,
            "solar_current_a": 6.7,
            "link_margin_db": 12.9,
            "attitude_error_deg": 0.3,
        },
        "battery_voltage_history": [7.58, 7.60, 7.59, 7.59],
        "operator_note": "Textbook pass, no notes.",
    },
    {
        "pass_id": "PASS-009",
        "timestamp": "2026-06-25T15:50:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.48,
            "battery_temp_c": 20.1,
            "bus_voltage_v": 26.8,
            "solar_current_a": 6.0,
            "link_margin_db": 12.0,
            "attitude_error_deg": 0.5,
        },
        "battery_voltage_history": [7.55, 7.52, 7.50, 7.48],
        "operator_note": "Bus voltage looked a touch low on the live plot but I didn't think much of it.",
    },
    {
        "pass_id": "PASS-010",
        "timestamp": "2026-06-25T17:25:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.50,
            "battery_temp_c": 18.9,
            "bus_voltage_v": 30.0,
            "solar_current_a": 6.3,
            "link_margin_db": 13.1,
            "attitude_error_deg": 0.2,
        },
        "battery_voltage_history": [7.49, 7.51, 7.50, 7.50],
        "operator_note": "All parameters steady, quiet shift.",
    },
    {
        "pass_id": "PASS-011",
        "timestamp": "2026-06-25T19:00:00Z",
        "eclipse": True,
        "telemetry": {
            "battery_voltage_v": 6.55,
            "battery_temp_c": 13.0,
            "bus_voltage_v": 29.0,
            "solar_current_a": 0.05,
            "link_margin_db": 10.4,
            "attitude_error_deg": -0.4,
        },
        "battery_voltage_history": [7.20, 6.95, 6.70, 6.55],
        "operator_note": "Battery is lower than I'd like coming out of eclipse but solar charging looks like it's catching up okay.",
    },
    {
        "pass_id": "PASS-012",
        "timestamp": "2026-06-25T20:35:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.61,
            "battery_temp_c": 50.8,
            "bus_voltage_v": 30.3,
            "solar_current_a": 7.0,
            "link_margin_db": 13.5,
            "attitude_error_deg": 0.3,
        },
        "battery_voltage_history": [7.60, 7.62, 7.61, 7.61],
        "operator_note": "Quick pass, looked fine to me, moving on to next contact.",
    },
    {
        "pass_id": "PASS-013",
        "timestamp": "2026-06-25T22:10:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.57,
            "battery_temp_c": 18.0,
            "bus_voltage_v": 30.1,
            "solar_current_a": 6.5,
            "link_margin_db": 13.0,
            "attitude_error_deg": 0.1,
        },
        "battery_voltage_history": [7.56, 7.58, 7.57, 7.57],
        "operator_note": "Nominal across the board.",
    },
    {
        "pass_id": "PASS-014",
        "timestamp": "2026-06-25T23:45:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.20,
            "battery_temp_c": 21.5,
            "bus_voltage_v": 29.8,
            "solar_current_a": 5.8,
            "link_margin_db": 11.5,
            "attitude_error_deg": 0.6,
        },
        "battery_voltage_history": [7.62, 7.50, 7.35, 7.20],
        "operator_note": "Continuing the slow battery decline I noted a few passes back, still within limits but the trend is consistent now.",
    },
    {
        "pass_id": "PASS-015",
        "timestamp": "2026-06-26T01:20:00Z",
        "eclipse": False,
        "telemetry": {
            "battery_voltage_v": 7.55,
            "battery_temp_c": 19.2,
            "bus_voltage_v": 30.2,
            "solar_current_a": 6.6,
            "link_margin_db": 1.8,
            "attitude_error_deg": 0.2,
        },
        "battery_voltage_history": [7.57, 7.56, 7.56, 7.55],
        "operator_note": "Link looked unstable on the waterfall, lots of dropouts, but everything else reads fine.",
    },
]
