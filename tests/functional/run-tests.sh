#!/usr/bin/env bash
## Run functional tests.

## The output files are tracked, so changes in the results will be shown
## in the status.

if [[ -n $(git status -s) ]]; then
    printf 'Working tree should be clean for tests.\n'
    exit 1
fi

testdir=test-results
mkdir -p $testdir
testfile=$testdir/test-output

printf '* DY - last name column\n' > $testfile
wcut death-years.txt last >> $testfile
printf '* DY - last name column, complement\n' >> $testfile
wcut -v death-years.txt last >> $testfile
printf '* DY - last name column, only delimiter\n' >> $testfile
wcut -s death-years.txt last >> $testfile
printf '* DY - last name column, wholename, no match\n' >> $testfile
wcut -w death-years.txt last >> $testfile
printf '* DY - last name column, wholename\n' >> $testfile
wcut -w death-years.txt last_name >> $testfile
printf '* DY - year and first name column, reverse order\n' >> $testfile
wcut death-years.txt year first >> $testfile

printf '* WM - config column\n' >> $testfile
wcut -d',' -l2 tiling-wms.csv Config >> $testfile
printf '* WM - config column, wrong match line\n' >> $testfile
wcut -d',' -l1 tiling-wms.csv Config &>> $testfile
printf '* WM - config column, no preheader\n' >> $testfile
wcut -d',' -l2 -r tiling-wms.csv Config >> $testfile
printf '* WM - config column, complement\n' >> $testfile
wcut -d',' -l2 -v tiling-wms.csv Config >> $testfile
printf '* WM - config column, only delimiter\n' >> $testfile
wcut -d',' -l2 -s tiling-wms.csv Config >> $testfile
printf '* WM - config column, ignore case\n' >> $testfile
wcut -d',' -l2 -i tiling-wms.csv Config >> $testfile
printf '* WM - config column, wholename, no match\n' >> $testfile
wcut -d',' -l2 -w tiling-wms.csv Config >> $testfile
printf '* WM - config column, wholename\n' >> $testfile
wcut -d',' -l2 -w tiling-wms.csv "Configured with" >> $testfile
printf '* WM - written in and window manager, reverse order\n' >> $testfile
wcut -d',' -l2 tiling-wms.csv Writ Man >> $testfile
printf '* WM - written in and window manager, reverse order, ignore case\n' >> $testfile
wcut -d',' -l2 -i tiling-wms.csv writ man >> $testfile

printf '* STDIN - first col\n' >> $testfile
printf "first second third\n1 2 3\n4 5 6" | wcut - first >> $testfile

## Outfile test
wcut death-years.txt last -o $testdir/dy-lastname-outfile

if [[ -z $(git status -s) ]]; then
    printf 'Tests passed.\n'
else
    printf 'Some tests failed.\n'
    exit 2
fi
