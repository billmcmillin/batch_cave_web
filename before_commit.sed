s/print.*//g
s/\ utilities/\ self.utilities/g
s/.*utilities.SaveToMRK(recs, filename)//g
s/utilities.MakeMARCFile(recs, filename)/self.utilities.CreateMRC(recs)/g
# run with sed -i -f before_commit.sed batchEdits.py
