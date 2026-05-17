import typer

from resources.pod.collector import collect_pod_data
from resources.deployment.collector import collect_deployment_data
from resources.service.collector import collect_service_data
from resources.ingress.collector import collect_ingress_data
from resources.node.collector import collect_node_data

from gemini_client import analyze_incident
from formatter import print_output

app = typer.Typer()


@app.command()
def analyze(
    resource: str = typer.Option(...),
    name: str = typer.Option(...),
    namespace: str = typer.Option("default")
):

    if resource == "pod":

        data = collect_pod_data(
            namespace,
            name
        )

    elif resource == "deployment":

        data = collect_deployment_data(
            namespace,
            name
        )
    
    elif resource == "service":

        data = collect_service_data(
            namespace,
            name
    )

    elif resource == "ingress":

        data = collect_ingress_data(
            namespace,
            name
    )

    elif resource == "node":

        data = collect_node_data(
            name
    )

    else:

        print("Unsupported resource")
        raise typer.Exit()

    analysis = analyze_incident(data)

    print_output(analysis)


if __name__ == "__main__":
    app()