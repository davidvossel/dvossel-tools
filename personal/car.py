#!/usr/bin/env python
import os
import sys

def examples():

	print "---- EXAMPLES ----"
	print "./car.py <price> <mileage/1000> <avg_mpg>\n"

	print "New $19000 Civic, ./car.py 19000 0 31"
	print "\t$1266.00 Yearly value over 15 years"
	print "\t$1207.00 Yearly gas expense at 10000 miles a year"
	print "\t$2473.00 YEARLY COST (not counting mainteance)"


def main(argv):
	if len(argv) < 4:
		examples()
		print "BAD USAGE look at examples above ^^^"
		return -1

	price = int(argv[1])
	mileage = int(argv[2])
	avg_mpg = int(argv[3])

	max_mileage = 175
	max_years = 15
	avg_yearly_mileage = 10

	if mileage > 300:
		mileage = mileage / 1000

	years_owning_car = (max_mileage - mileage) / avg_yearly_mileage
	if years_owning_car > max_years:
		years_owning_car = max_years
	elif years_owning_car < 1:
		years_owning_car = 1

	yearly_value = price / years_owning_car
	yearly_gas = ((avg_yearly_mileage * 1000) / avg_mpg) * 3.75
	total_cost = price + (yearly_gas * years_owning_car)

	print "--- RESULTS ----"
	print "\t%d Years of usage can be expected" % (years_owning_car)
	print "\t$%d.00 Yearly value over %d years" % (yearly_value, years_owning_car)
	print "\t$%d.00 Yearly gas expense at %d miles a year" % (yearly_gas, (avg_yearly_mileage * 1000))
	print "\t$%d.00 YEARLY COST (not counting mainteance)" % (yearly_value + yearly_gas)

	if years_owning_car < 7:
		print "WARNING: expected life span less than 7 years"
	if (yearly_value + yearly_gas) > 3500:
		print "WARNING: Yearly cost is over $3500, and that sucks"

	print "\n--- Compare yearly expense results  --- "
	print "~$3300 = New CR-V"
	print "~$2500 = New Civic"
	print "$%d = Your Results" % (yearly_value + yearly_gas)
	print "\n"


if __name__=="__main__":
	main(sys.argv)
