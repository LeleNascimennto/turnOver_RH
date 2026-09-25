import config
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri(config.URI_TRACKING)
cliente = MlflowClient()

modelos = cliente.search_model_versions(
    "name='{}'".format(config.NOME_MODELO)
)

for modelo in modelos:
    print(
        f"versao={modelo.version} | "
        f"run_id={modelo.run_id}"
    )