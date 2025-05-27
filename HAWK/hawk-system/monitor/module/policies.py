
# Политики безопасности
policies = (
    # {"src": "....", "dst": "....", "opr": "...."}

    {"src": "video-service", "dst": "data-collector", "opr": "send_video"},
    {"src": "telemetry", "dst": "data-collector", "opr": "send_telemetry"},
    {"src": "telemetry", "dst": "validator", "opr": "send_telemetry"},
    {"src": "data-collector", "dst": "validator", "opr": "data_to_valid"},
    {"src": "validator", "dst": "chipher", "opr": "send_to_chipher"},
    {"src": "chipher", "dst": "communication", "opr": "send"},
    {"src": "communication", "dst": "communication-volan", "opr": "send_to_volan"},

    {"src": "communication-volan", "dst": "chipher-volan", "opr": "send_data"},
    {"src": "chipher-volan", "dst": "analysis-volan", "opr": "data_to_process"},
    {"src": "analysis-volan", "dst": "distributor-volan", "opr": "distribute-event"},
    {"src": "analysis-volan", "dst": "communication-volan", "opr": "person_to_access"},
    {"src": "distributor-volan", "dst": "communication-volan", "opr": "to_security"},
    {"src": "distributor-volan", "dst": "communication-volan", "opr": "to_repair"},
    {"src": "communication-volan", "dst": "communication-grif", "opr": "to_grif"},
    {"src": "communication-volan", "dst": "communication-repair", "opr": "data_to_repair"},

    {"src": "communication-repair", "dst": "handle-repair", "opr": "send_data"},
    {"src": "handle-repair", "dst": "activate-repair", "opr": "activate"},
    {"src": "activate-repair", "dst": "analysis-repair", "opr": "analysis"},
    {"src": "analysis-repair", "dst": "start-repair", "opr": "repair"},
    {"src": "start-repair", "dst": "communication-repair", "opr": "ready_repair"},
    {"src": "communication-repair", "dst": "communication-volan", "opr": "repair_report"},

    {"src": "communication-grif", "dst": "chipher-grif", "opr": "send_data"},
    {"src": "chipher-grif", "dst": "communication-grif", "opr": "valid_data"}
)

def check_operation(id, details) -> bool:
    """ Проверка возможности совершения обращения. """
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    opr: str = details.get("operation")

    if not all((src, dst, opr)):
        return False

    print(f"[info] checking policies for event {id},  {src}->{dst}: {opr}")

    return {"src": src, "dst": dst, "opr": opr} in policies
