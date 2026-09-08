#+-----------------------------------+
#| Created by: fgatto13 @2026-02-06  |
#+-----------------------------------+
# function_app.py
import azure.functions as func
from patients import (
    get_patient_route,
    patients_route,       # combined GET + POST
    update_patient_route
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register routes
app.route(route="patients/{patient_id}", methods=["GET"])(get_patient_route)
app.route(route="patients", methods=["GET", "POST", "OPTIONS"])(patients_route)
app.route(route="patients/{patient_id}", methods=["PUT", "OPTIONS"])(update_patient_route)
