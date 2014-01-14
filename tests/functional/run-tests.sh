#!/usr/bin/env bash
## Run functional tests.

## The output files are tracked, so changes in the results will be shown
## in the status.

testdir=test-results
mkdir -p $testdir
testfile=$testdir/test-output

printf '* DY - last name column\n' > $testfile
wcut last death-years.txt >> $testfile
printf '* DY - last name column, complement\n' >> $testfile
wcut last -v death-years.txt >> $testfile
printf '* DY - last name column, only delimiter\n' >> $testfile
wcut last -s death-years.txt >> $testfile
printf '* DY - last name column, wholename, no match\n' >> $testfile
wcut last -w death-years.txt >> $testfile
printf '* DY - last name column, wholename\n' >> $testfile
wcut last_name -w death-years.txt >> $testfile
printf '* DY - year and first name column, reverse order\n' >> $testfile
wcut year,first death-years.txt >> $testfile

printf '* WM - config column\n' >> $testfile
wcut -d',' -l2 Config tiling-wms.csv >> $testfile
printf '* WM - config column, wrong match line\n' >> $testfile
wcut -d',' -l1 Config tiling-wms.csv &>> $testfile
printf '* WM - config column, no preheader\n' >> $testfile
wcut -d',' -l2 -r Config tiling-wms.csv >> $testfile
printf '* WM - config column, complement\n' >> $testfile
wcut -d',' -l2 -v Config tiling-wms.csv >> $testfile
printf '* WM - config column, only delimiter\n' >> $testfile
wcut -d',' -l2 -s Config tiling-wms.csv >> $testfile
printf '* WM - config column, ignore case\n' >> $testfile
wcut -d',' -l2 -i config tiling-wms.csv >> $testfile
printf '* WM - config column, wholename, no match\n' >> $testfile
wcut -d',' -l2 -w Config tiling-wms.csv >> $testfile
printf '* WM - config column, wholename\n' >> $testfile
wcut -d',' -l2 -w "Configured with" tiling-wms.csv >> $testfile
printf '* WM - written in and window manager, reverse order\n' >> $testfile
wcut -d',' -l2 Writ,Man tiling-wms.csv >> $testfile
printf '* WM - written in and window manager, reverse order, ignore case\n' >> $testfile
wcut -d',' -l2 -i writ,man tiling-wms.csv >> $testfile

printf '* STDIN - first col\n' >> $testfile
printf "first second third\n1 2 3\n4 5 6" | wcut first - >> $testfile

## Outfile test
wcut last death-years.txt -o $testdir/dy-lastname-outfile
