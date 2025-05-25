
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
    {"src": "distributor-volan", "dst": "communication-volan", "opr": "to_security"},
    {"src": "distributor-volan", "dst": "communication-volan", "opr": "to_repair"}
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
