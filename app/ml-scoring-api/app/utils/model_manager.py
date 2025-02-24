import onnxruntime

# Load ONNX models for issuer and acquirer flows
issuer_model = onnxruntime.InferenceSession("issuer_model.onnx")
acquirer_model = onnxruntime.InferenceSession("acquirer_model.onnx")

async def score_transaction(transaction_features, scoring_flow):
    """
    Scores the transaction using ONNX Runtime.
    """
    if scoring_flow == 'issuer':
        model = issuer_model
    elif scoring_flow == 'acquirer':
        model = acquirer_model
    else:
        raise ValueError("Invalid scoring flow")

    # Prepare input for ONNX model
    #...

    # Score the transaction
    score = model.run(None, input_feed)

    return score
