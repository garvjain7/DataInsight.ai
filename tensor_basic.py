import tensorflow as tf

a = tf.constant([1, 2, 3])
b = tf.constant([4, 5, 6])

add_result = tf.add(a, b)
mul_result = tf.multiply(a, b)

print("Tensor a:", a.numpy())
print("Tensor b:", b.numpy())
print("Addition:", add_result.numpy())
print("Multiplication:", mul_result.numpy())
