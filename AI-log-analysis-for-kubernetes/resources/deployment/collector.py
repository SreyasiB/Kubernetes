import json

from resources.shared.command import run_command
from resources.shared.parsers import extract_events_section


def get_deployment_selector(namespace, deployment_name):

    command = (
        f"kubectl get deployment {deployment_name} "
        f"-n {namespace} -o json"
    )

    output = run_command(command)

    try:

        deployment_json = json.loads(output)

        selectors = deployment_json["spec"]["selector"]["matchLabels"]

        selector_string = ",".join(
            [f"{k}={v}" for k, v in selectors.items()]
        )

        return selector_string

    except Exception:

        return None


def collect_related_pods(namespace, selector):

    if not selector:
        return "No selector found"

    command = (
        f"kubectl get pods -n {namespace} "
        f"-l {selector}"
    )

    return run_command(command)


def collect_deployment_data(namespace, deployment_name):

    rollout_status = run_command(
        f"kubectl rollout status deployment/{deployment_name} -n {namespace}"
    )

    describe_output = run_command(
        f"kubectl describe deployment {deployment_name} -n {namespace}"
    )

    deployment_events = extract_events_section(
        describe_output
    )

    selector = get_deployment_selector(
        namespace,
        deployment_name
    )

    related_pods = collect_related_pods(
        namespace,
        selector
    )

    cluster_events = run_command(
        f"kubectl get events -n {namespace} --sort-by=.lastTimestamp | tail -20"
    )

    context = f"""
ROLLOUT STATUS:
{rollout_status}

DEPLOYMENT EVENTS:
{deployment_events}

RELATED PODS:
{related_pods}

CLUSTER EVENTS:
{cluster_events}
"""

    return {
        "resource_type": "deployment",
        "context": context
    }