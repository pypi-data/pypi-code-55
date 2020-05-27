import numpy as np

t = np.logspace(-1, 1, 20)
Gt = np.exp(-t)
np.savetxt(
    "test.gt",
    np.transpose([t, Gt]),
    header="Mw=0;gamma=1;\n# GenerateMaxwellData.py",
    comments="",
)
w = np.logspace(-1, 1, 20)
Gp = w ** 2 / (1 + w ** 2)
Gpp = w / (1 + w ** 2)
np.savetxt(
    "test.tts",
    np.c_[w, Gp, Gpp],
    header="Mw=0;T=0;\n# GenerateMaxwellData.py",
    comments="",
)

