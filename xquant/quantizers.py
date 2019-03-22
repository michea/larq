import tensorflow as tf
from xquant import utils


@utils.register_keras_custom_object
@tf.custom_gradient
def sign_ste(x):
    def grad(dy):
        return dy

    return tf.sign(x), grad


@utils.register_keras_custom_object
@tf.custom_gradient
def approx_sign(x):
    def grad(dy):
        return (1 - tf.abs(x)) * 2 * dy

    return tf.sign(x), grad


@utils.register_keras_custom_object
def approx_sign_clip(x):
    return approx_sign(tf.clip_by_value(x, -1, 1))


@utils.register_keras_custom_object
def sign_clip_ste(x):
    return sign_ste(tf.clip_by_value(x, -1, 1))


def serialize(initializer):
    return tf.keras.utils.serialize_keras_object(initializer)


def deserialize(name, custom_objects=None):
    return tf.keras.utils.deserialize_keras_object(
        name,
        module_objects=globals(),
        custom_objects=custom_objects,
        printable_module_name="quantization function",
    )


def get(identifier):
    if identifier is None:
        return None
    if isinstance(identifier, str):
        return deserialize(str(identifier))
    if callable(identifier):
        return identifier
    raise ValueError(
        "Could not interpret quantization function identifier:", identifier
    )
