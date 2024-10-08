cd /tmp
touch hsperfdata_s466468
wc -m ~/lab0/bellossom4/monferno ~/lab0/sawsbuck6/cottonee ~/lab0/sawsbuck6/frillish ~/lab0/sawsbuck6/whiscash ~/lab0/sawsbuck6/starly ~/lab0/zorua8/diglett > /tmp/hsperfdata_s466468
cd ~

ls -lR lab0 2>>/tmp/hsperfdata_s466468 | grep '6$' | sort -k6 -r

cat ~/lab0/bellossom4/archen ~/lab0/bellossom4/chimchar ~/lab0/bellossom4/monferno ~/lab0/sawsbuck6/cottonee ~/lab0/sawsbuck6/frillish ~/lab0/sawsbuck6/whiscash ~/lab0/sawsbuck6/starly | grep -n "mb"

cat ~/lab0/bellossom4/monferno ~/lab0/sawsbuck6/cottonee ~/lab0/sawsbuck6/frillish ~/lab0/sawsbuck6/whiscash 2>>/tmp/hsperfdata_s466468 | grep "ci"

ls -lR lab0 2>&1 | grep '^d' | sort -k6 | tail -n2

cat ~/lab0/bellossom4/monferno ~/lab0/sawsbuck6/cottonee ~/lab0/sawsbuck6/frillish ~/lab0/sawsbuck6/whiscash | nl | sort -r
