from app.dame_perceval import DamePerceval


gg = DamePerceval()
n = gg.numCommits("https://github.com/davidam/davidam.git",
                  "/tmp/clonedir")
print(n)
l = gg.list_committers(
                "https://github.com/davidam/davidam.git",
                "/tmp/clonedir")
print(l)

ll = gg.list_committers2(
                "https://github.com/davidam/davidam.git",
                "/tmp/clonedir")
print(ll)
