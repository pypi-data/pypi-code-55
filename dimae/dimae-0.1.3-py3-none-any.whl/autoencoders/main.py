from dimae.autoencoders import AE

a = AE(n_input = 80, code_nodes = 10, summary=False)
# a.fit()
encoder = a.generate_encoder()
encoder.summary()
