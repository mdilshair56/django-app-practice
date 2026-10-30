from django.db import models


def get_unique_constraint_fields(model, constraint_name):
    model_meta = getattr(model, "_meta")

    for constraint in model_meta.constraints:
        if constraint.name == constraint_name:
            if isinstance(constraint, models.UniqueConstraint):
                return list(constraint.fields)

            raise ValueError(
                f"'{constraint_name}' is not a UniqueConstraint"
            )

    raise ValueError(
        f"Constraint '{constraint_name}' not found on {model.__name__}"
    )