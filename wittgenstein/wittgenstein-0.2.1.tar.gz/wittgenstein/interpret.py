from wittgenstein.base_functions import score_accuracy, try_np_tonum

def interpret_model(
    model,
    X,
    interpreter,
    model_prediction_function=None,
    resolution_function=score_accuracy
):
    """Interpret a more complex model."""

    if not model_prediction_function:
        model_preds = model.predict(X)
    else:
        model_preds = try_np_tonum(model_prediction_function(model, X)) # in case predictions come out in an unexpected format (cough cough, tf)

    interpreter.fit(X, model_preds)
    resolution = interpreter.score(X, model_preds, resolution_function)
    interpreter.base_model = model
    return interpreter, resolution
