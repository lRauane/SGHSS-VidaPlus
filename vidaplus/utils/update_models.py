def update_model_instance(instance, data: dict):
    for field, value in data.items():
        setattr(instance, field, value)
