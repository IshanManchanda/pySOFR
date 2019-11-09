import context


def next_roll(section, roll_number, x, error):
	roll_number += 1
	if not x:
		error += 1
	else:
		error = 0

	if error > context.STUDENTS_PER_SECTION:
		roll_number -= context.STUDENTS_PER_SECTION + 1
		section += 1
		error = 0
	return section, roll_number, error
