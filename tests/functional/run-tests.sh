#!/usr/bin/env bash
## Run functional tests

## The output files are tracked, so changes in the results will be shown
## in the status

testdir=test-results
mkdir -p $testdir
testfile=$testdir/test-output

echo '* DY - last name column' > $testfile
wcut last death-years.txt >> $testfile
echo '* DY - last name column, complement' >> $testfile
wcut last -v death-years.txt >> $testfile
echo '* DY - last name column, only delimiter' >> $testfile
wcut last -s death-years.txt >> $testfile
echo '* DY - last name column, wholename, no match' >> $testfile
wcut last -w death-years.txt >> $testfile
echo '* DY - last name column, wholename' >> $testfile
wcut last_name -w death-years.txt >> $testfile
echo '* DY - year and first name column, reverse order' >> $testfile
wcut year,first death-years.txt >> $testfile

echo '* WM - config column' >> $testfile
wcut -d',' -l2 Config tiling-wms.csv >> $testfile
echo '* WM - config column, wrong match line' >> $testfile
wcut -d',' -l1 Config tiling-wms.csv &>> $testfile
echo '* WM - config column, no preheader' >> $testfile
wcut -d',' -l2 -r Config tiling-wms.csv >> $testfile
echo '* WM - config column, complement' >> $testfile
wcut -d',' -l2 -v Config tiling-wms.csv >> $testfile
echo '* WM - config column, only delimiter' >> $testfile
wcut -d',' -l2 -s Config tiling-wms.csv >> $testfile
echo '* WM - config column, ignore case' >> $testfile
wcut -d',' -l2 -i config tiling-wms.csv >> $testfile
echo '* WM - config column, wholename, no match' >> $testfile
wcut -d',' -l2 -w Config tiling-wms.csv >> $testfile
echo '* WM - config column, wholename' >> $testfile
wcut -d',' -l2 -w "Configured with" tiling-wms.csv >> $testfile
echo '* WM - written in and window manager, reverse order' >> $testfile
wcut -d',' -l2 Writ,Man tiling-wms.csv >> $testfile
echo '* WM - written in and window manager, reverse order, ignore case' >> $testfile
wcut -d',' -l2 -i writ,man tiling-wms.csv >> $testfile

echo '* STDIN - first col' >> $testfile
echo -e "first second third\n1 2 3\n4 5 6" | wcut first - >> $testfile

## out file test
wcut last death-years.txt -o $testdir/dy-lastname-outfile
