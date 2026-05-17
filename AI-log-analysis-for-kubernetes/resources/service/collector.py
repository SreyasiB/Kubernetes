import json

from resources.shared.command import run_command
from resources.shared.parsers import extract_events_section


def get_service_selector(namespace, service_name):

    command = (
        f"kubectl get svc {service_name} "
        f"-n {namespace} -o json"
    )

    output = run_command(command)

    try:

        service_json = json.loads(output)

        selectors = service_json["spec"]["selector"]

        selector_string = ",".join(
            [f"{k}={v}" for k, v in selectors.items()]
        )

        return selector_string

    except Exception:

        return None


def collect_matching_pods(namespace, selector):

    if not selector:
        return "No selector found"

    command = (
        f"kubectl get pods -n {namespace} "
        f"-l {selector} -o wide"
    )

    return run_command(command)


def collect_service_endpoints(namespace, service_name):

    command = (
        f"kubectl get endpoints {service_name} "
        f"-n {namespace}"
    )

    return run_command(command)


def collect_service_data(namespace, service_name):

    describe_output = run_command(
        f"kubectl describe svc {service_name} -n {namespace}"
    )

    service_events = extract_events_section(
        describe_output
    )

    selector = get_service_selector(
        namespace,
        service_name
    )

    matching_pods = collect_matching_pods(
        namespace,
        selector
    )

    endpoints = collect_service_endpoints(
        namespace,
        service_name
    )

    cluster_events = run_command(
        f"kubectl get events -n {namespace} --sort-by=.lastTimestamp | tail -20"
    )

    context = f"""
SERVICE EVENTS:
{service_events}

ENDPOINTS:
{endpoints}

MATCHING PODS:
{matching_pods}

CLUSTER EVENTS:
{cluster_events}
"""

    return {
        "resource_type": "service",
        "context": context
    }