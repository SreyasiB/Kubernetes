from resources.shared.command import run_command
from resources.shared.parsers import extract_events_section


def collect_pod_data(namespace, pod_name):

    logs = run_command(
        f"kubectl logs {pod_name} -n {namespace} --tail=50"
    )

    describe_output = run_command(
        f"kubectl describe pod {pod_name} -n {namespace}"
    )

    describe_events = extract_events_section(
        describe_output
    )

    cluster_events = run_command(
        f"kubectl get events -n {namespace} --sort-by=.lastTimestamp | tail -20"
    )

    context = f"""
LOGS:
{logs}

POD EVENTS:
{describe_events}

CLUSTER EVENTS:
{cluster_events}
"""

    return {
        "resource_type": "pod",
        "context": context
    }