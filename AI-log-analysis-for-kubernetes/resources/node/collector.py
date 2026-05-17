import json

from resources.shared.command import run_command
from resources.shared.parsers import extract_events_section


def get_node_conditions(node_name):

    command = (
        f"kubectl get node {node_name} -o json"
    )

    output = run_command(command)

    try:

        node_json = json.loads(output)

        conditions = node_json["status"]["conditions"]

        formatted_conditions = []

        for condition in conditions:

            formatted_conditions.append(
                f"""
TYPE: {condition['type']}
STATUS: {condition['status']}
REASON: {condition.get('reason', 'N/A')}
MESSAGE: {condition.get('message', 'N/A')}
"""
            )

        return "\n".join(formatted_conditions)

    except Exception:

        return "Unable to fetch node conditions"


def get_pods_on_node(node_name):

    command = (
        f"kubectl get pods -A "
        f"--field-selector spec.nodeName={node_name} "
        f"-o wide"
    )

    return run_command(command)


def collect_node_data(node_name):

    describe_output = run_command(
        f"kubectl describe node {node_name}"
    )

    node_events = extract_events_section(
        describe_output
    )

    node_conditions = get_node_conditions(
        node_name
    )

    pods_on_node = get_pods_on_node(
        node_name
    )

    cluster_events = run_command(
        "kubectl get events -A --sort-by=.lastTimestamp | tail -20"
    )

    context = f"""
NODE CONDITIONS:
{node_conditions}

NODE EVENTS:
{node_events}

PODS RUNNING ON NODE:
{pods_on_node}

CLUSTER EVENTS:
{cluster_events}
"""

    return {
        "resource_type": "node",
        "context": context
    }