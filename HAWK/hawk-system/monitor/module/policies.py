
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
    {"src": "communication-volan", "dst": "communication-sec", "opr": "data_to_sec"},

    {"src": "communication-sec", "dst": "chipher-sec", "opr": "send_data"},
    {"src": "chipher-sec", "dst": "handler-sec", "opr": "valid_data"},
    {"src": "chipher-sec", "dst": "validator-sec", "opr": "hash_value"},
    {"src": "handler-sec", "dst": "activate-sec", "opr": "activate"},
    {"src": "activate-sec", "dst": "events-sec", "opr": "analysis"},
    {"src": "events-sec", "dst": "distributor-sec", "opr": "send_data"},
    {"src": "distributor-sec", "dst": "validator-sec", "opr": "to_valid"},
    {"src": "validator-sec", "dst": "communication-robot", "opr": "to_robot"},
    {"src": "communication-sec", "dst": "communication-volan", "opr": "report_robot"},

    {"src": "communication-robot", "dst": "chipher-robot", "opr": "send_data"},
    {"src": "chipher-robot", "dst": "control-sys-robot", "opr": "valid_data"},
    {"src": "chipher-robot", "dst": "controller-robot", "opr": "hash_value"},
    {"src": "control-sys-robot", "dst": "drivers-robot", "opr": "pull"},
    {"src": "drivers-robot", "dst": "control-sys-robot", "opr": "push"},
    {"src": "control-sys-robot", "dst": "nav-robot", "opr": "get_nav"},
    {"src": "nav-robot", "dst": "control-sys-robot", "opr": "send_coords"},
    {"src": "control-sys-robot", "dst": "controller-robot", "opr": "to_valid"},
    {"src": "controller-robot", "dst": "gear-robot", "opr": "valid_data"},
    {"src": "gear-robot", "dst": "control-sys-robot", "opr": "report_to_sys"},
    {"src": "control-sys-robot", "dst": "speakers-robot", "opr": "to_audio"},
    {"src": "speakers-robot", "dst": "communication-robot", "opr": "report_robot"},
    {"src": "communication-robot", "dst": "communication-sec", "opr": "report_robot"},

    {"src": "communication-repair", "dst": "handle-repair", "opr": "send_data"},
    {"src": "handle-repair", "dst": "activate-repair", "opr": "activate"},
    {"src": "activate-repair", "dst": "analysis-repair", "opr": "analysis"},
    {"src": "analysis-repair", "dst": "start-repair", "opr": "repair"},
    {"src": "start-repair", "dst": "communication-repair", "opr": "ready_repair"},
    {"src": "communication-repair", "dst": "communication-volan", "opr": "repair_report"},

    {"src": "communication-grif", "dst": "chipher-grif", "opr": "send_data"},
    {"src": "chipher-grif", "dst": "communication-grif", "opr": "valid_data"},
    {"src": "chipher-grif", "dst": "communication-grif", "opr": "to_reboot"},
    {"src": "communication-grif", "dst": "handler-grif", "opr": "send_data"},
    {"src": "handler-grif", "dst": "poweroff-grif", "opr": "send_command"},
    {"src": "poweroff-grif", "dst": "communication-grif", "opr": "report_off"},

    {"src": "user", "dst": "authentication", "opr": "send_pass"},
    {"src": "user", "dst": "validator-card", "opr": "send_card"},
    {"src": "authentication", "dst": "authorization", "opr": "auth"},
    {"src": "validator-card", "dst": "authorization", "opr": "auth_card"},
    {"src": "authorization", "dst": "handle-command", "opr": "send_command"},
    {"src": "handle-command", "dst": "chipher-terminal", "opr": "to_chipher"},
    {"src": "chipher-terminal", "dst": "communication-terminal", "opr": "send"},
    {"src": "communication-terminal", "dst": "communication-vetrolov", "opr": "to_vetrolov"},

    {"src": "communication-vetrolov", "dst": "chipher-vetrolov", "opr": "to_valid"},
    {"src": "chipher-vetrolov", "dst": "handler-vetrolov", "opr": "command_to_process"},
    {"src": "handler-vetrolov", "dst": "generator-vetrolov", "opr": "poweroff"},
    {"src": "generator-vetrolov", "dst": "controller-vetrolov", "opr": "send_status"},
    {"src": "controller-vetrolov", "dst": "battery-vetrolov", "opr": "send_command"},
    {"src": "battery-vetrolov", "dst": "communication-vetrolov", "opr": "send_status"},
    {"src": "communication-vetrolov", "dst": "chipher-vetrolov", "opr": "to_diagnostic"},
    {"src": "chipher-vetrolov", "dst": "communication-vetrolov", "opr": "hash_data"},
    {"src": "communication-vetrolov", "dst": "communication-diagnostic", "opr": "to_diagnostic"},

    {"src": "communication-diagnostic", "dst": "chipher-diagnostic", "opr": "to_valid"},
    {"src": "chipher-diagnostic", "dst": "validator-diagnostic", "opr": "to_valid"},
    {"src": "validator-diagnostic", "dst": "camera-diagnostic", "opr": "asking"},
    {"src": "camera-diagnostic", "dst": "validator-diagnostic", "opr": "answer"},
    {"src": "validator-diagnostic", "dst": "chipher-diagnostic", "opr": "to_grif"},
    {"src": "chipher-diagnostic", "dst": "communication-diagnostic", "opr": "hash_data"},
    {"src": "communication-diagnostic", "dst": "communication-grif", "opr": "to_grif_off"}
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
