import json

from resources.shared.command import run_command
from resources.shared.parsers import extract_events_section


def get_backend_services(namespace, ingress_name):

    command = (
        f"kubectl get ingress {ingress_name} "
        f"-n {namespace} -o json"
    )

    output = run_command(command)

    try:

        ingress_json = json.loads(output)

        services = []

        rules = ingress_json["spec"].get("rules", [])

        for rule in rules:

            paths = rule["http"]["paths"]

            for path in paths:

                service_name = path["backend"]["service"]["name"]

                services.append(service_name)

        return list(set(services))

    except Exception:

        return []


def collect_backend_service_details(namespace, services):

    if not services:
        return "No backend services found"

    results = []

    for service in services:

        svc_output = run_command(
            f"kubectl get svc {service} -n {namespace}"
        )

        endpoint_output = run_command(
            f"kubectl get endpoints {service} -n {namespace}"
        )

        results.append(
            f"""
SERVICE:
{service}

SERVICE DETAILS:
{svc_output}

ENDPOINTS:
{endpoint_output}
"""
        )

    return "\n".join(results)


def collect_ingress_data(namespace, ingress_name):

    describe_output = run_command(
        f"kubectl describe ingress {ingress_name} -n {namespace}"
    )

    ingress_events = extract_events_section(
        describe_output
    )

    backend_services = get_backend_services(
        namespace,
        ingress_name
    )

    backend_details = collect_backend_service_details(
        namespace,
        backend_services
    )

    cluster_events = run_command(
        f"kubectl get events -n {namespace} --sort-by=.lastTimestamp | tail -20"
    )

    context = f"""
INGRESS EVENTS:
{ingress_events}

BACKEND SERVICE DETAILS:
{backend_details}

CLUSTER EVENTS:
{cluster_events}
"""

    return {
        "resource_type": "ingress",
        "context": context
    }